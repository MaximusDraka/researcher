from fastapi import FastAPI
from pydantic import BaseModel
import json
import pickle
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

import os
from pathlib import Path
from dotenv import load_dotenv

import spacy
from spacy.util import filter_spans
from spacy import displacy

import pandas as pd

from utils.neo4j.connection import Neo4jConnection
from utils.neo4j import query
from utils import logger_util, monitor_util, kb_util
from models import recommender_model, classification_model



def missing_skills(conn: Neo4jConnection, profiles: any, my_skills: list) -> tuple[str, pd.DataFrame]:
        
    if type(profiles) is not pd.DataFrame:
        chosen_profile = profiles[0]
    else:
        chosen_profile = profiles.iloc[0]['profile']    

    to_learn = query.get_remaining_skills_by_profile(conn, chosen_profile, my_skills)
         
    return chosen_profile, to_learn


def extract_skills(data: str, conn: Neo4jConnection, nlp: any, loaded_matcher: any, NER_type: str) -> tuple[any, pd.DataFrame]:


    #Evaluate A - Ruler version
    if NER_type == 'A':       
        doc = nlp(data)
       
        tags = list(ent.text.lower() for ent in doc.ents if ent.label_ == 'SKILL')
           
    #Evaluate   - Matcher version before NER Model is trained
    if NER_type == 'B':
        doc = nlp(data)
        matches = loaded_matcher(doc, as_spans=True)
        filtered_spans =spacy.util.filter_spans(matches)
        doc.ents = filter_spans(filtered_spans)              
       
        tags = list(ent.text.lower() for ent in doc.ents if ent.label_ == 'SKILL')
        
    #Evaluate C - Trained annoted model   
    if NER_type == 'C':
        doc = nlp(data)
       
        tags = list(ent.text.lower() for ent in doc.ents if ent.label_ == 'SKILL')    
               
    no_duplicates_list = list(set(tags))  
    
    return doc, no_duplicates_list


def config_app(NER_type: str) -> tuple[logger_util.Logger_util, monitor_util.Monitor, Neo4jConnection, any, any, str, str]:
    # Load the stored environment variables ########################################################################
    load_dotenv()

    app_logger, monitor, conn, nlp, loaded_matcher = None, None, None, None, None

    # Setup #########################################################################################################

    app_logger = logger_util.Logger_util(os.getenv("LOG_FILE"))
    monitor = monitor_util.Monitor(os.getenv("MONITOR_FILE"))

    conn = Neo4jConnection(uri=os.getenv("DB_URI"), 
                        user=os.getenv("DB_USERNAME"),              
                        pwd=os.getenv("DB_PASSWORD"))
    
    config=""
    meta=""
    
    # Load the NER model    
    if NER_type == 'A':
        NER_model = 'ruler_model'
        nlp = spacy.load("./models/NER/%s" % (NER_model))
        config = nlp.config.to_str()
        meta=nlp.meta
    
    if NER_type == 'B':
        nlp = spacy.load("en_core_web_sm")
        nlp.vocab.strings.add('SKILL')        
        filename = "./models/NER/finalized_matcher.pickle"
        file = Path(filename)
        
        if file.is_file():
            loaded_matcher = pickle.load(open(filename, 'rb'))
        else: 
            db_skills = query.get_all_skills(conn)
            abbreviations = kb_util.get_abbreviations()
            skills_and_abbreviations = db_skills + abbreviations
            kb_util.create_matcher_from_db(filename, skills_and_abbreviations, save=True)
            loaded_matcher = pickle.load(open(filename, 'rb'))      
            
    
    if NER_type == 'C':
        NER_model = 'model-best-C_PT_E_HP_P'
        nlp = spacy.load("./models/NER/%s" % (NER_model))
        config = nlp.config.to_str()
        meta=nlp.meta
        
    return app_logger, monitor, conn, nlp, loaded_matcher, config, meta


class ApplicationInput(BaseModel):
    data: str
    ner_type: str
    scenario: str
    to_be_profile: str
    show_displacy: bool
    recommender_type: str
    classification_type: str


class ApplicationOutput(BaseModel):
    status: str
    skills: list
    skills_to_learn: str    
    profiles: dict
    courses: dict
    displacy_html: str
    config: str
    meta: dict

app = FastAPI()

@app.get("/gettopskillsbyprofile")
async def gettopskillsbyprofile_endpoint(profile: str="Data Analyst"):
    load_dotenv()
    conn = Neo4jConnection(uri=os.getenv("DB_URI"), 
                        user=os.getenv("DB_USERNAME"),              
                        pwd=os.getenv("DB_PASSWORD"))
   
    df_data = query.get_skills_by_profile(conn, profile) 
    
    response = df_data.to_dict()
    
    return JSONResponse(content=jsonable_encoder(response)) 


@app.get("/obtainlogasJSON")
async def obtainlogasJSON_endpoint(filename: str="./data/log/monitor.jsonl"):
    data = [] 
    with open(filename) as f:        
         for line in f:
            data.append(json.loads(line))   
    
    return JSONResponse(content=jsonable_encoder(data))  


@app.post("/recommendcourses", response_model=ApplicationOutput)
async def recommendcourses_endpoint(user_input: ApplicationInput):
    
    
    displacy_html_content = ""
    
    if user_input.ner_type == 'Ruler':
        ner_type = 'A'
    if user_input.ner_type == 'Matcher':
        ner_type = 'B'
    if user_input.ner_type == 'Trained NER':
        ner_type = 'C'
    
    if user_input.scenario == 'Improve existing profile with current skills':
        scenario = 'A'
    if user_input.scenario == 'Improve existing profile with missing skills':     
        scenario = 'B'
    if user_input.scenario == 'Become a specific profile':
        scenario = 'C'
    
   
    if user_input.classification_type == 'Python code':
        classification_type = 'A1'
    if user_input.classification_type == 'Cypher query':
        classification_type = 'A2'
    if user_input.classification_type == 'text classification':
        classification_type = 'B' 
    
    to_be_profile = user_input.to_be_profile
    recommender_type = user_input.recommender_type
    show_displacy = user_input.show_displacy
    
    #Configure application
    app_logger, monitor, conn, nlp, loaded_matcher, config, meta  = config_app(ner_type)
    
    doc, skills = extract_skills(user_input.data, conn, nlp, loaded_matcher, ner_type)
    
    if len(skills) == 0:
           return ApplicationOutput(status="ERROR",skills=[],skills_to_learn="",profiles={},courses={},displacy_html="",config="",meta="")
    else:
               
        if show_displacy: 
                                  
            options = {"ents": ["SKILL"]}                       
            
            displacy_html_content = displacy.render(
                doc,
                style="ent",
                options=options
            )           
        
        
        if scenario == 'A' or scenario == 'B':
            # Define profile
            if classification_type == 'A1':
                profiles = classification_model.profiles_A1(conn, skills)
            if classification_type == 'A2':           
                profiles = classification_model.profiles_A2(conn, skills)     
            if classification_type == 'B':
                profiles = recommender_model.profiles_B(conn, skills)          
                
        else:
            profiles = [to_be_profile]

        if profiles is None:          
            
            return ApplicationOutput(status="ERROR",skills=[],skills_to_learn="",profiles={},courses={},displacy_html="",config="",meta="")
        else:    
            # Search for missing skills for the profile
            if scenario == 'B' or scenario == 'C':
                chosen_profile, df_skills_to_learn = missing_skills(conn, profiles, skills)                
                skill_to_learn = ' '.join([x for x in df_skills_to_learn['skill']])
            else:
                chosen_profile = profiles.iloc[0]['profile']
                skill_to_learn = ' '.join([x for x in skills])  
                       
            
            if recommender_type == 'tfidf-data':
                # Get all courses from the database to use the full data
                courses = query.get_all_courses(conn)
                field = 'data'
            if recommender_type == 'tfidf-skills':
                # Get all courses from the database with a list of skills
                courses = query.get_all_courses_with_skills(conn)
                field = 'skills'

            if recommender_type == 'tfidf-data' or recommender_type == 'tfidf-skills':          
                # Get recommended courses           
                recommended_courses = recommender_model.courses_tfidf(courses, field, skill_to_learn, 5)
            else:
                if scenario == 'A':
                    recommended_courses = recommender_model.courses_cypher(conn, skills, 5)
                else:
                    recommended_courses = recommender_model.courses_cypher(conn, df_skills_to_learn['skill'], 5)                           
           
                    
            if scenario == 'C':
                log_profiles= {"profile": {"0": chosen_profile}}
            else:
                log_profiles = profiles.to_dict()    
    
    
    monitor.write_to_log(scenario,user_input.data,ner_type,skills,log_profiles,recommended_courses.to_dict(),classification_type,recommender_type,to_be_profile)
    app_logger.logger.info('Webapp finished running')
    
    
    return ApplicationOutput(status="SUCCESS",
                             skills=skills, 
                             skills_to_learn=skill_to_learn,                              
                             profiles=log_profiles, 
                             courses=recommended_courses.to_dict(),
                             displacy_html=displacy_html_content,
                             config=config,
                             meta=meta)    