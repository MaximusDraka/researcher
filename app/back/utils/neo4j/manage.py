import time
import query as query
import pandas as pd
from connection import Neo4jConnection


def refresh_all_profile_skill_scores(conn: Neo4jConnection):
    
    for profile in query.get_all_profiles(conn):
        print(profile)
        
        total_objects_for_profile = query.get_edge_count_by_profile(conn, profile, 'IS')
        print('Total objects for ' + profile + ': ' + str(total_objects_for_profile))
        
        df_skills = query.get_all_skills_by_profile(conn, profile)
        
        if df_skills.empty:
            continue
    
        df_skills['profile'] = profile   
        df_skills['score'] = df_skills['skill'].apply(lambda x: query.get_edge_count_by_profile_skill(conn, profile, x) / total_objects_for_profile*100)
        
        print(df_skills.sort_values(by='score', ascending=False))
        
        set_profile_skill_score(conn, df_skills, batch_size=10000)


def insert_data(conn: Neo4jConnection, query: str, rows: pd.DataFrame, batch_size: int=10000, parameters: dict=None) -> dict:
    
    # Function to handle the updating the Neo4j database in batch mode.

    total = 0
    batch = 0
    start = time.time()
    result = None

    while batch * batch_size < len(rows):

        if parameters is None:
            param = {'rows': rows[batch*batch_size:(batch+1)*batch_size].to_dict('records')}        
        else:
            param = parameters | {'rows': rows[batch*batch_size:(batch+1)*batch_size].to_dict('records')}

        print(param)
        
        res = conn.query(query, parameters=param)
        total += res[0]['total']
        batch += 1
        result = {"total":total, "batches":batch, "time":time.time()-start}
        print(result)

    return result


def set_profile_skill_score(conn: Neo4jConnection, rows : pd.DataFrame, batch_size: int=10000) -> dict:
                 
    query = '''
    UNWIND $rows AS row    
    MATCH (p:Profile {name: row.profile})-[r:HAS]-(s:Skill {name: row.skill})    
    SET r.score = row.score   
    RETURN count(*) as total
    '''    
    return insert_data(conn, query, rows, batch_size)