import streamlit as st
import json
import requests
import base64
from utils import util
from streamlit_tags import st_tags
import pandas as pd
from altair import *


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
   return requests.post(url="http://skillskeletonapi:8000/recommendcourses", data=json.dumps(inputs))   
                      
     


def get_log_file():
    response = requests.get(url="http://skillskeletonapi:8000/obtainlogasJSON")   
                      
    return response.json()    

def get_skills(profile):
    response = requests.get(url="http://skillskeletonapi:8000/gettopskillsbyprofile", params={'profile': profile})   
                      
    return response.json()



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
                save_image_path = './Uploaded_Resumes/' + pdf_file.name
                with open(save_image_path, "wb") as f:
                    f.write(pdf_file.getbuffer())
                
                    show_pdf(save_image_path)           
                    cv_content = read_resume(save_image_path)        
                      
                      
                inputs = {"data": cv_content, "ner_type": ner_type, "scenario": scenario, "to_be_profile": to_be_profile, "show_displacy": show_displacy, "recommender_type": recommender_type, "classification_type": recommender_type}
                
                response = get_response(inputs)                                
                response = response.json()                  
                
                status = response['status']
                skills = response['skills']
                df_profiles = pd.DataFrame(response['profiles'])                    
                df_courses = pd.DataFrame(response['courses'])
                displacy_html = response['displacy_html']
                
                config =  response['config']
                meta =  response['meta']
                
                if status == 'SUCCESS':
                    
                
                    with col2:
                        
                        st.title("Results")
                        
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
                    
                        st.subheader('Profile results')          
                        #st.dataframe(df_profiles)
                        
                        data = pd.melt(df_profiles, id_vars=['profile'], value_vars=['count', 'max', 'coverage', 'total_score'], var_name='Genre', value_name='Score')
                        
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
                        
                        if scenario == 'Improve existing profile with missing skills' or scenario == 'Improve existing profile with current skills':
                            st.subheader('Detected profile') 
                            st.info('Profile is chosen based on coverage DESC, total DESC')
                        else:
                            st.subheader('Requested new profile') 
                        st.write(df_profiles.iloc[0]['profile'])               
                                                            
                                        
                        st.subheader('Recommended courses') 
                        st.markdown(df_courses.to_html(render_links=True),unsafe_allow_html=True)  
                        
                       
                         
                else:
                    st.error('Skills not detected')                     
                    
    
    if choice == 'Data Engineer':
        st.success('Welcome Data Engineer')
        st.subheader('Model logs')  
           
        response = get_log_file()             
       
        df_log = pd.DataFrame(response)
        df_log['date'] = pd.to_datetime(df_log['date'],dayfirst=True)
    
        mask = (df_log['date'].dt.date == pd.Timestamp.today().date())
        df_today = df_log[mask]
        
        st.metric(label="Usage", value=df_log.shape[0], delta=df_today.shape[0], delta_color="inverse")
        
        st.dataframe(df_log)

    if choice == 'Data Analyst':
        
        response_DA = get_skills("Data Analyst")
        df_DA = pd.DataFrame(response_DA)
        
        response_DE = get_skills("Data Engineer")
        df_DE = pd.DataFrame(response_DE)
        
        response_DS = get_skills("Data Scientist")
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