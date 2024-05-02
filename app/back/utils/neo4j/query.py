import pandas as pd
import random
from utils.neo4j.connection import Neo4jConnection


def get_total_skill_count_by_profile(profile_name: str,conn: Neo4jConnection, min_score: int=5) -> int:
    
    parameters = {'profile_name': profile_name,'min_score': min_score}

    query_string = '''
    MATCH (p:Profile {name: $profile_name})-[r:HAS]->(s:Skill)
    WHERE r.score > $min_score
    RETURN count(s) as total
    '''
    return conn.query(query_string,parameters=parameters)[0]['total']


def get_skills_by_profile_and_category(conn: Neo4jConnection, profile_name: str, category_name: str, min_score: int=5) -> pd.DataFrame:
    
    parameters = {'profile_name': profile_name,
                  'category_name': category_name,
                  'min_score': min_score
                  }

    query_string = '''
    MATCH (p:Profile {name: $profile_name})-[r:HAS]->(s:Skill) 
    WHERE r.score > $min_score AND s.category = $category_name
    RETURN p.name as profile, s.name as skill, r.score as score
    ORDER BY score DESC
    '''
    return pd.DataFrame([dict(_) for _ in conn.query(query_string,parameters=parameters)])


def get_score_by_skills(conn: Neo4jConnection, skills: list, min_score: int=5) -> pd.DataFrame:
    
    parameters = {'skills': skills, 'min_score': min_score}

    query_string = '''
    MATCH (p:Profile)-[r:HAS]->(s:Skill) 
    WHERE r.score > $min_score AND toLower(s.name) in $skills
    RETURN p.name as profile, s.name as skill, r.score as score
    ORDER BY score DESC
    '''
    return pd.DataFrame([dict(_) for _ in conn.query(query_string,parameters=parameters)])


def get_remaining_skills_by_profile(conn: Neo4jConnection, profile_name: str, skills: list, min_score: int=5, limit: int=10) -> pd.DataFrame:
    
    parameters = {'profile_name': profile_name,
                  'skills': skills,
                  'min_score': min_score,
                  'limit': limit
                  }       
    
    query_string = '''
    MATCH (p:Profile {name: $profile_name})-[r:HAS]->(s:Skill) 
    WHERE r.score > $min_score AND not s.name in $skills
    RETURN s.name as skill, r.score as score
    ORDER BY score DESC LIMIT $limit
    '''
    return pd.DataFrame([dict(_) for _ in conn.query(query_string,parameters=parameters)])


def get_all_for_graph(conn: Neo4jConnection,profile_name: str) -> pd.DataFrame:   

    parameters = {'profile_name': profile_name}

    query_string = '''
    MATCH (p:Profile {name: $profile_name})-[r:HAS]->(s:Skill) 
    WHERE s.category = 'Tools' RETURN *
    '''
    return conn.query(query_string,response_type="graph",parameters=parameters)


def get_10_random_skills(conn: Neo4jConnection) -> list[str]:   

    query_string = '''
    MATCH (s:Skill)  RETURN s.name
    '''    
    all_skills = [record.get("s.name") for record in conn.query(query_string)]    
    return random.sample(all_skills, 10)  


def get_all_skills(conn: Neo4jConnection) -> list[str]:   

    query_string = '''
    MATCH (s:Skill)  RETURN s.name
    '''        
    return [record.get("s.name") for record in conn.query(query_string)]


def get_all_profiles(conn: Neo4jConnection) -> list[str]:   

    query_string = '''
    MATCH (p:Profile)  RETURN p.name
    '''        
    return [record.get("p.name") for record in conn.query(query_string)] 


def get_all_skills_by_profile(conn: Neo4jConnection, profile_name: str) -> pd.DataFrame:
    
    parameters = {'profile_name': profile_name}

    query_string = '''
    MATCH (p:Profile {name: $profile_name})-[r:HAS]->(s:Skill)    
    RETURN s.name as skill   
    '''
    return pd.DataFrame([dict(_) for _ in conn.query(query_string,parameters=parameters)])


def get_skills_by_profile(conn: Neo4jConnection, profile_name: str, min_score: int=5,top: int=10) -> pd.DataFrame:
    
    parameters = {'profile_name': profile_name,                  
                  'min_score': min_score,
                   'limit': top
                  }

    query_string = '''
    MATCH (p:Profile {name: $profile_name})-[r:HAS]->(s:Skill) 
    WHERE r.score > $min_score
    RETURN p.name as profile, s.name as skill, r.score as score
    ORDER BY score DESC LIMIT $limit
    '''
    return pd.DataFrame([dict(_) for _ in conn.query(query_string,parameters=parameters)])


def get_edge_count_by_profile(conn: Neo4jConnection,profile_name: str, relationship: str) -> int:
    
    parameters = {'profile_name': profile_name, 'relationship': relationship}

    query_string = '''
    MATCH (p:Profile {name: $profile_name})-[r]-(o)    
    WHERE type(r) = $relationship
    RETURN count(r) as total
    '''
    return conn.query(query_string,parameters=parameters)[0]['total']


def get_edge_count_by_profile_skill(conn: Neo4jConnection, profile_name: str, skill_name: str) -> int:
    
    parameters = {'profile_name': profile_name, 'skill_name': skill_name}
      
    query_string = '''
    MATCH (p:Profile {name: $profile_name})-[IS]-(o) 
    RETURN sum(COUNT { (o)-[:CONTAINS]-(s:Skill {name: $skill_name})}) as total
    '''
    return conn.query(query_string,parameters=parameters)[0]['total']


def get_all_courses(conn: Neo4jConnection) -> pd.DataFrame:   

    query_string = '''
    MATCH (c:Course) RETURN c.title as title, c.url as url, c.data as data, c.language as language
    '''
    return pd.DataFrame([dict(_) for _ in conn.query(query_string)])


def get_all_courses_with_skills(conn: Neo4jConnection) -> pd.DataFrame:
    
    query_string = '''
    MATCH (c:Course)-[r:OFFERS]-(s:Skill) RETURN collect(s.name) as skills,c.title as title, c.url as url, c.data as data, c.language as language
     '''
    return pd.DataFrame([dict(_) for _ in conn.query(query_string)])


def get_all_profiles_with_skills(conn: Neo4jConnection, min_score: int=5) -> pd.DataFrame:
    
    parameters = {'min_score': min_score}    
    
    query_string = '''
    MATCH (p:Profile)-[r:HAS]-(s:Skill) WHERE r.score > $min_score RETURN p.name as profile, collect(s.name) as skills
     '''
    return pd.DataFrame([dict(_) for _ in conn.query(query_string,parameters=parameters)])


def get_recommended_profile(conn: Neo4jConnection, skills: list, min_score: int=5) -> pd.DataFrame:
    
    parameters = {'skills': skills, 'min_score': min_score}
    
    query_string = '''
    MATCH(s:Skill)-[r:HAS]-(p:Profile)
    WHERE s.name in $skills AND r.score > $min_score
    RETURN p.name as profile, count(r) as connections, 
    COUNT{(s2:Skill)-[r2:HAS]-(p2:Profile) WHERE p2.name=p.name AND r2.score > $min_score} as all_skills, toFloat(count(r))/COUNT{(s3:Skill)-[r3:HAS]-(p3:Profile) WHERE p3.name=p.name AND r3.score > $min_score}*100 as coverage, sum(r.score) as total_score
    ORDER BY coverage DESC, total_score DESC
    '''
    return pd.DataFrame(conn.query(query_string,parameters=parameters),columns=['profile','count','max','coverage','total_score'])


def get_recommended_courses(conn: Neo4jConnection, skills: list, num_recommendations: int=5) -> pd.DataFrame:
    
    parameters = {'skills': skills, 'num_recommendations': num_recommendations}
    
    query_string = '''
    MATCH (c:Course)-[r:OFFERS]-(s:Skill) 
    WHERE s.name IN $skills
    RETURN c.title as title,c.url as url, count(s) as total
    ORDER BY total DESC
    LIMIT $num_recommendations
    '''
    return pd.DataFrame([dict(_) for _ in conn.query(query_string,parameters=parameters)])


def get_courses_with_many_skills(conn: Neo4jConnection, num_recommendations: int=5) -> pd.DataFrame:
    
    parameters = {'num_recommendations': num_recommendations}

    query_string = '''
    MATCH (c:Course)-[o:OFFERS]->(s:Skill)
    WITH c, count(*) as skills
    WHERE skills > 10
    RETURN c.title as title,c.url as url, skills as total
    ORDER BY skills desc 
    LIMIT $num_recommendations
    '''
    return pd.DataFrame([dict(_) for _ in conn.query(query_string,parameters=parameters)])