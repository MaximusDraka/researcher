import pandas as pd
from utils.neo4j import query
from utils.neo4j.connection import Neo4jConnection


def profiles_A1(conn: Neo4jConnection,my_skills: list) -> pd.DataFrame:     
    
    # Get all skill scores from the database linked to all profiles
    profile_score = query.get_score_by_skills(conn, my_skills)

    if profile_score.empty:
        return None
    else:
               
        
        #Count all skills for each profile
        match_profile_count = profile_score.groupby(['profile'])['profile'].value_counts()        
        df = pd.DataFrame({'profile':match_profile_count.index, 'count':match_profile_count.values})

        #Sum all scores for each profile
        match_profile_total_score = profile_score.groupby(['profile'])['score'].sum()
        df2 = pd.DataFrame({'profile':match_profile_total_score.index, 'total_score':match_profile_total_score.values})

        #Get the maximum number of skills for each profile
        df['max'] = df['profile'].apply(query.get_total_skill_count_by_profile, conn=conn)
        
        #Percentage of how many skills the resume has compared to the maximum number of skills for each profile
        df['coverage'] = (df['count'] / df['max'])*100

        merged_df = df.merge(df2, on="profile")

        #Sort by coverage and total score
        #Define the best profile for the list of found skills based on the skills coverage for the profile and afterwards when equal look at total skill score by profile        
        merged_df.sort_values(by=['coverage', 'total_score'], ascending=[False,False], inplace=True)
                            
        return merged_df


def profiles_A2(conn: Neo4jConnection,my_skills: list) -> pd.DataFrame:     
    
    return query.get_recommended_profile(conn,my_skills)