import pandas as pd
from connection import Neo4jConnection


def get_degree(conn: Neo4jConnection,graph_name: str) -> pd.DataFrame: 

    parameters = {'graph_name': graph_name}

    query_string = '''
    CALL gds.degree.stream('$graph_name',{ relationshipWeightProperty: 'score' })
    YIELD nodeId, score
    RETURN gds.util.asNode(nodeId).name AS name, score AS weightedFollowers    
    ORDER BY weightedFollowers DESC, name DESC
    '''
    return pd.DataFrame([dict(_) for _ in conn.query(query_string,parameters=parameters)])


def get_closeness(conn: Neo4jConnection,graph_name: str) -> pd.DataFrame: 

    parameters = {'graph_name': graph_name}

    query_string = '''
    CALL gds.closeness.stream('$graph_name')
    YIELD nodeId, score
    RETURN gds.util.asNode(nodeId).name AS name, score   
    ORDER BY score DESC, name DESC
    '''    
    return pd.DataFrame([dict(_) for _ in conn.query(query_string,parameters=parameters)])


def get_betweenness(conn: Neo4jConnection,graph_name: str) -> pd.DataFrame: 

    parameters = {'graph_name': graph_name}

    query_string = '''
    CALL gds.betweenness.stream('$graph_name')
    YIELD nodeId, score
    RETURN gds.util.asNode(nodeId).name AS name, score
    ORDER BY name ASC
    '''
    return pd.DataFrame([dict(_) for _ in conn.query(query_string,parameters=parameters)])