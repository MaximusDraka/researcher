import streamlit as st
import json
import requests
import base64
from utils import util
from streamlit_tags import st_tags
import pandas as pd
from altair import *

from pydantic import BaseModel
import json
import pickle

import os
from pathlib import Path

import spacy
from spacy.util import filter_spans
from spacy import displacy

from utils.neo4j.connection import Neo4jConnection
from utils.neo4j import query
from utils import logger_util, monitor_util, kb_util
from models import recommender_model, classification_model

from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

def missing_skills(conn: Neo4jConnection, profiles: any, my_skills: list) -> tuple[str, pd.DataFrame]:
        
    if type(profiles) is not pd.DataFrame:
        chosen_profile = profiles[0]
    else:
        chosen_profile = profiles.iloc[0]['profile']    

    to_learn = query.get_remaining_skills_by_profile(conn, chosen_profile, my_skills)
         
    return chosen_profile, to_learn


def extract_skills(data: str, conn: Neo4jConnection, nlp: any, loaded_matcher: any, NER_type: str) -> tuple[any, list[str]]:


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
   
    app_logger, monitor, conn, nlp, loaded_matcher = None, None, None, None, None

    # Setup #########################################################################################################

    app_logger = logger_util.Logger_util(st.secrets["LOG_FILE"])
    monitor = monitor_util.Monitor(st.secrets["MONITOR_FILE"])

    conn = Neo4jConnection(uri=st.secrets["DB_URI"], 
                        user=st.secrets["DB_USERNAME"],              
                        pwd=st.secrets["DB_PASSWORD"])
    
    config=""
    meta=""
    
    # Load the NER model    
    if NER_type == 'A':
        NER_model = 'ruler_model'
        nlp = spacy.load("/mount/src/skill-skeleton/cloud-app/models/NER/%s" % (NER_model))
        config = nlp.config.to_str()
        meta=nlp.meta
    
    if NER_type == 'B':
        nlp = spacy.load("en_core_web_sm")
        nlp.vocab.strings.add('SKILL')        
        filename = "/mount/src/skill-skeleton/cloud-app/models/NER/finalized_matcher.pickle"
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
        nlp = spacy.load("/mount/src/skill-skeleton/cloud-app/models/NER/%s" % (NER_model))
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


def gettopskillsbyprofile(profile: str="Data Analyst"):
   
    conn = Neo4jConnection(uri=st.secrets["DB_URI"], 
                        user=st.secrets["DB_USERNAME"],              
                        pwd=st.secrets["DB_PASSWORD"])
   
    df_data = query.get_skills_by_profile(conn, profile)   
    
    return df_data


def obtainlogasJSON(filename: str="/mount/src/skill-skeleton/cloud-app/data/log/monitor.jsonl"):
    data = [] 
    with open(filename) as f:        
         for line in f:
            data.append(json.loads(line))   
    
    return data


def recommendcourses(user_input: dict):
    
    displacy_html_content = ""
    
    if user_input["ner_type"] == 'Ruler':
        ner_type = 'A'
    if user_input["ner_type"] == 'Matcher':
        ner_type = 'B'
    if user_input["ner_type"] == 'Trained NER':
        ner_type = 'C'
    
    if user_input["scenario"] == 'Improve existing profile with current skills':
        scenario = 'A'
    if user_input["scenario"] == 'Improve existing profile with missing skills':     
        scenario = 'B'
    if user_input["scenario"] == 'Become a specific profile':
        scenario = 'C'
    
   
    if user_input["classification_type"] == 'Python code':
        classification_type = 'A1'
    if user_input["classification_type"] == 'Cypher query':
        classification_type = 'A2'
    if user_input["classification_type"] == 'text classification':
        classification_type = 'B' 
    
    to_be_profile = user_input["to_be_profile"]
    recommender_type = user_input["recommender_type"]
    show_displacy = user_input["show_displacy"]
    
    #Configure application
    app_logger, monitor, conn, nlp, loaded_matcher, config, meta  = config_app(ner_type)
    
    doc, skills = extract_skills(user_input["data"], conn, nlp, loaded_matcher, ner_type)
    
    if len(skills) == 0:
           
            log_profiles= {"profile": {"0": None}}
            recommended_courses = query.get_courses_with_many_skills(conn, 5)            

            monitor.write_to_log(scenario,user_input["data"],ner_type,skills,log_profiles,recommended_courses.to_dict(),classification_type,recommender_type,to_be_profile)
            app_logger.logger.info('Webapp finished running - no skills found in the resume')
    
            return ApplicationOutput(status="NO_SKILLS_FOUND",
                                    skills=[], 
                                    skills_to_learn="",                              
                                    profiles={}, 
                                    courses=recommended_courses.to_dict(),
                                    displacy_html="",
                                    config=config,
                                    meta=meta)    


          
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
            
            return ApplicationOutput(status="NO_PROFILE_FOUND",skills=[],skills_to_learn="",profiles={},courses={},displacy_html="",config="",meta="")
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
    
    
    monitor.write_to_log(scenario,user_input["data"],ner_type,skills,log_profiles,recommended_courses.to_dict(),classification_type,recommender_type,to_be_profile)
    app_logger.logger.info('Webapp finished running')
    
    
    return ApplicationOutput(status="SUCCESS",
                             skills=skills, 
                             skills_to_learn=skill_to_learn,                              
                             profiles=log_profiles, 
                             courses=recommended_courses.to_dict(),
                             displacy_html=displacy_html_content,
                             config=config,
                             meta=meta)    


def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')   
    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)


def read_resume(file_path: str) -> str:
    
    file_content = util.read_PDF(file_path)    
    #Remove punctuation from the data
    file_content = util.fix(file_content)
        
    return file_content


def get_html(html: str):
    """Convert HTML so it can be rendered."""
    WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem; margin-bottom: 2.5rem">{}</div>"""
    # Newlines seem to mess with the rendering
    html = html.replace("\n", " ")
    return WRAPPER.format(html)


@st.cache_data()
def get_response(inputs):
   return recommendcourses(inputs)                         



def run():    
    st.set_page_config(
    page_title="Skill Skeleton App",
    page_icon="☠️",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://github.com/MaximusDraka/skill-skeleton',
        'Report a bug': "https://github.com/MaximusDraka/skill-skeleton",
        'About': "# Skill Skeleton. From CV to course recommendations"})
    
        
    st.sidebar.markdown("# Choose Profile")
    activities = ["Application User", "Data Engineer", "Data Analyst"]
    choice = st.sidebar.selectbox("Choose among the given options:", activities)

    if choice == 'Application User': 
        
        col1, col2 = st.columns([2, 3]) 
        
        with col1:
            
            st.title("Skill Skeleton App ☠️")
            
            st.subheader('Configuration')
            
            ner_types = ["Ruler", "Matcher", "Trained NER"]
            ner_type = st.selectbox("The NER type to use", ner_types,2)
            
            scenarios = ["Improve existing profile with current skills", "Improve existing profile with missing skills", "Become a specific profile"]
            scenario = st.selectbox("The application scenario", scenarios,1)
            
            profiles = ["Data Analyst", "Data Engineer", "Data Scientist"]
            to_be_profile = st.selectbox("The profile to become for scenario C", profiles,0)
            
            show_tags = ["True", "False"]
            show_displacy = st.selectbox("Show displacy skills from PDF", show_tags,0)
            
            recommender_types = ["tfidf-data", "tfidf-skills","cypher-skills"]
            recommender_type = st.selectbox("The recommender type to use", recommender_types,2)
            
            classification_types = ["Python code", "Cypher query","text classification"]
            recommender_type = st.selectbox("The classification type to use", classification_types,1)            
            
            pdf_file = st.file_uploader("Choose your Resume", type=["pdf"])
        
            if pdf_file is not None:           
                save_image_path = '/mount/src/skill-skeleton/cloud-app/' + pdf_file.name
                with open(save_image_path, "wb") as f:
                    f.write(pdf_file.getbuffer())
                
                    show_pdf(save_image_path)           
                    cv_content = read_resume(save_image_path)        
                      
                      
                inputs = {"data": cv_content, "ner_type": ner_type, "scenario": scenario, "to_be_profile": to_be_profile, "show_displacy": show_displacy, "recommender_type": recommender_type, "classification_type": recommender_type}
                
                response = get_response(inputs).model_dump()                    
                                
                status = response['status']
                skills = response['skills']
                df_profiles = pd.DataFrame(response['profiles'])                    
                df_courses = pd.DataFrame(response['courses'])
                displacy_html = response['displacy_html']
                
                config =  response['config']
                meta =  response['meta']
                
                with col2:

                    st.title("Results")

                    if status == 'SUCCESS':  
                        
                        if ner_type != 'Matcher':
                            st.subheader('Model Information') 
                            
                            meta_exp = st.expander("Pipeline meta.json")
                            meta_exp.json(meta)
        
                            config_exp = st.expander("Pipeline config.cfg")
                            config_exp.code(config)                        
                        
                        st.success('Skills detected successfully')
                        
                        if show_displacy == 'True':
                            st.subheader('NER Tags') 
                            style = "<style>mark.entity { display: inline-block }</style>"
                            st.write(f"{style}{get_html(displacy_html)}", unsafe_allow_html=True)                    
                        
                        
                        detected_skills = st_tags(label='### Skills that you have',
                                            text='',
                                            value=skills, key='1')
                        
                        if scenario == 'Improve existing profile with missing skills' or scenario == 'Become a specific profile':
                            if response['skills_to_learn']:                         
                                missing_skills = st_tags(label='### Skills that you want to learn',
                                            text='',
                                            value=response['skills_to_learn'].split(), key='2')                       
                                
                        
                        if scenario == 'Improve existing profile with missing skills' or scenario == 'Improve existing profile with current skills':
                            data = pd.melt(df_profiles, id_vars=['profile'], value_vars=['count', 'max', 'coverage', 'total_score'], var_name='Genre', value_name='Score')

                            st.subheader('Profile results') 

                            c = (
                                Chart(data).mark_bar().encode(
                                column=Column('Genre'),
                                x=X('profile'),
                                y=Y('Score'),
                                color=Color('Genre', scale=Scale(range=['#EA98D2', '#659CCA', '#F6C85F', '#7CC272']))
                                ).configure_view(
                                    strokeWidth=0.0,
                                ) 
                            )
                            st.altair_chart(c, use_container_width=False) 

                            st.subheader('Detected profile') 
                            st.info('Profile is chosen based on coverage DESC, total DESC')
                        else:
                            st.subheader('Requested new profile') 
                        st.write(df_profiles.iloc[0]['profile'])               
                                                            
                                        
                        st.subheader('Recommended courses') 
                        st.markdown(df_courses.to_html(render_links=True),unsafe_allow_html=True)                          
                    
                    if status == 'NO_SKILLS_FOUND':
                        st.error('No skills detected')
                        
                        st.subheader('Recommended general courses') 
                        st.markdown(df_courses.to_html(render_links=True),unsafe_allow_html=True) 
                            
                    if status == 'NO_PROFILE_FOUND':
                        st.error('No profile detected')            
                    
    
    if choice == 'Data Engineer':
        st.success('Welcome Data Engineer')
        st.subheader('Model logs')  
           
        response = obtainlogasJSON()             
       
        df_log = pd.DataFrame(response)
        df_log['date'] = pd.to_datetime(df_log['date'],dayfirst=True)
    
        mask = (df_log['date'].dt.date == pd.Timestamp.today().date())
        df_today = df_log[mask]
        
        st.metric(label="Usage", value=df_log.shape[0], delta=df_today.shape[0], delta_color="inverse")
        
        st.dataframe(df_log)

    if choice == 'Data Analyst':
        
        response_DA = gettopskillsbyprofile("Data Analyst")
        df_DA = pd.DataFrame(response_DA)
        
        response_DE = gettopskillsbyprofile("Data Engineer")
        df_DE = pd.DataFrame(response_DE)
        
        response_DS = gettopskillsbyprofile("Data Scientist")
        df_DS = pd.DataFrame(response_DS)
        
        with st.container():
            st.success('Welcome Data Analyst')
            st.subheader('Profile skills')
            
            col1, col2 = st.columns([1, 1]) 
        
            with col1:
                st.dataframe(df_DA)             
            with col2:    
                da = (
                    Chart(df_DA).mark_bar().encode(
                        x=X("score"),
                        y=Y("skill", sort="-x")
                    )
                )
            
                st.altair_chart(da, use_container_width=True)   
        
        with st.container():
            col1, col2 = st.columns([1, 1]) 
        
            with col1:
                st.dataframe(df_DE)
            with col2:    
                de = (
                    Chart(df_DE).mark_bar().encode(
                        x=X("score"),
                        y=Y("skill", sort="-x")
                    )
                )
            
                st.altair_chart(de, use_container_width=True)   
        
        with st.container():
            col1, col2 = st.columns([1, 1]) 
        
            with col1:
                st.dataframe(df_DS)
            with col2:
                ds = (
                    Chart(df_DS).mark_bar().encode(
                        x=X("score"),
                        y=Y("skill", sort="-x")
                    )
                )
                
                st.altair_chart(ds, use_container_width=True)            

run()