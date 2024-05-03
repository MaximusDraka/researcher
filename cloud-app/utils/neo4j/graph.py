import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from connection import Neo4jConnection


def drop_graph(conn: Neo4jConnection, graph_name: str):
       
    parameters = {'graph_name': graph_name}  
     
    query_string = '''
    CALL gds.graph.drop('$graph_name') YIELD graphName;
    '''
    conn.query(query_string,parameters=parameters)


def create_graph(conn: Neo4jConnection, graph_name: str):
       
    parameters = {'graph_name': graph_name}   
     
    query_string = '''
    CALL gds.graph.project(
    '$graph_name',
    ['Profile','Skill'],
    {
        HAS: {
        orientation: 'NATURAL',
        properties: ['score']
        }
    }
    )
    '''
    
    try:
        drop_graph(conn,graph_name)
    except:
        pass
    
    conn.query(query_string,parameters=parameters) 


def get_degree(conn: Neo4jConnection, graph_name: str) -> pd.DataFrame: 

    parameters = {'graph_name': graph_name}

    query_string = '''
    CALL gds.degree.stream('$graph_name',{ relationshipWeightProperty: 'score' })
    YIELD nodeId, score
    RETURN gds.util.asNode(nodeId).name AS name, score AS weightedFollowers    
    ORDER BY weightedFollowers DESC, name DESC
    '''
    return pd.DataFrame([dict(_) for _ in conn.query(query_string,parameters=parameters)])


def get_closeness(conn: Neo4jConnection, graph_name: str) -> pd.DataFrame: 

    parameters = {'graph_name': graph_name}

    query_string = '''
    CALL gds.closeness.stream('$graph_name')
    YIELD nodeId, score
    RETURN gds.util.asNode(nodeId).name AS name, score   
    ORDER BY score DESC, name DESC
    '''
    return pd.DataFrame([dict(_) for _ in conn.query(query_string,parameters=parameters)])


def get_betweenness(conn: Neo4jConnection, graph_name: str) -> pd.DataFrame: 

    parameters = {'graph_name': graph_name}

    query_string = '''
    CALL gds.betweenness.stream('$graph_name')
    YIELD nodeId, score
    RETURN gds.util.asNode(nodeId).name AS name, score
    ORDER BY name ASC
    '''
    return pd.DataFrame([dict(_) for _ in conn.query(query_string,parameters=parameters)])


def show_profile_score_graph(df: pd.DataFrame):
    
    plt.figure(figsize=(8,4))
    sns.barplot(x=df['profile'], y=df['score'])
    plt.xlabel('Profile', fontsize=12)
    plt.ylabel('Score',fontsize=12)
    plt.xticks(rotation='vertical', fontsize=10)
    plt.show()
    

def show_skill_score_graph(df: pd.DataFrame):
    
    plt.figure(figsize=(8,4))
    sns.barplot(x=df['skill'], y=df['score'])
    plt.xlabel('Skill', fontsize=12)
    plt.ylabel('Score',fontsize=12)
    plt.xticks(rotation='vertical', fontsize=10)
    plt.show()