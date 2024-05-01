from neo4j import GraphDatabase
import sys
from neo4j.debug import watch


class Neo4jConnection:
    
    def __init__(self, uri: str, user: str, pwd: str):
        self.__uri = uri
        self.__user = user
        self.__pwd = pwd
        self.__driver = None
        try:
            #watch("neo4j", out=sys.stdout)
            self.__driver = GraphDatabase.driver(self.__uri, auth=(self.__user, self.__pwd))
            self.__driver.verify_connectivity()                 
            
        except Exception as e:
            print("Failed to create the driver:", e)
        
        
    def close(self):
        if self.__driver is not None:
            self.__driver.close()
        
        
    def query(self, query: str, parameters: dict=None, db: str="neo4j", response_type: str="list") -> list:
        assert self.__driver is not None, "Driver not initialized!"
        session = None
        response = None
        try: 
            session = self.__driver.session(database=db) if db is not None else self.__driver.session()                     
                    
            if response_type == "graph":              
                #response = self.__driver.execute_query(query, result_transformer_=neo4j.Result.graph)
                response = session.run(query, parameters).graph()
            else:
                response = list(session.run(query, parameters))
        except Exception as e:
            print("Query failed:", e)
        finally: 
            if session is not None:
                session.close()
        return response