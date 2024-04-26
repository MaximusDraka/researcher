from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import pandas as pd
from utils.neo4j import query
from utils.neo4j.connection import Neo4jConnection

# Function that takes in skills to learn as input and outputs best courses to learn

def courses_tfidf(courses: pd.DataFrame, field: str, skills_to_learn: str, num_recommendations: int=10) -> pd.DataFrame:    
    
    #Only take English language
    df_en = courses[courses['language'] == 'English']
    if field == 'skills':    
        df_en[field] = [' '.join(map(str, l)) for l in df_en[field]]
                
    df_en = df_en[[field]]

    #Add skills to learn from profile to the dataframe
    new_record = pd.DataFrame([{field:skills_to_learn}])
                                
    df_full = pd.concat([df_en, new_record], ignore_index=True)       

    tfidf = TfidfVectorizer(stop_words='english')    
    tfidf_matrix = tfidf.fit_transform(df_full[field])
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    indices = pd.Series(df_full.index, index=df_full[field]).drop_duplicates()        
    
    idx = indices[skills_to_learn]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:num_recommendations+1]      
   
    return courses.iloc[[i[0] for i in sim_scores]]


def courses_cypher(conn: Neo4jConnection, skills_to_learn: list, num_recommendations: int=10) -> pd.DataFrame:
    return query.get_recommended_courses(conn, skills_to_learn, num_recommendations)


def profiles_B(conn: Neo4jConnection, my_skills: list) -> pd.DataFrame:
    
    df = query.get_all_profiles_with_skills(conn)    
    df['skills'] = [' '.join(map(str, l)) for l in df['skills']]    
    
    
    my_string = " ".join(str(element) for element in my_skills)
    
    new_record = pd.DataFrame([{'profile':'resume','skills':my_string}])                                
    df_full = pd.concat([df, new_record], ignore_index=True)   
    
    tfidf = TfidfVectorizer(stop_words='english')    
    tfidf_matrix = tfidf.fit_transform(df_full['skills'])
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    indices = pd.Series(df_full.index, index=df_full['skills']).drop_duplicates()       
        
    idx = indices[my_string]    
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:len(df)+1]
        
    return df_full.iloc[[i[0] for i in sim_scores]]