import json
import pandas as pd
from datetime import datetime
import pytz

class Monitor:    
    
    def __init__(self, file):
        self.file = file
    
    
    def write_to_log(self,scenario: str,resume: str,ner_model_version: str,skills: str,profiles: str,courses: str,classification_model_version: str,recommender_model_version: str, to_be_profile: str) -> str:    
        timezone = pytz.timezone('Europe/Brussels')
        now = datetime.now(tz = timezone)
        
        obj = {"date":now.strftime("%d/%m/%Y %H:%M:%S"),"scenario": scenario,"resume": resume, "ner_model_version": ner_model_version, "skills": skills, "profiles": profiles, "courses": courses, "classification_model_version": classification_model_version, "recommender_model_version": recommender_model_version, "to_be_profile": to_be_profile}

        with open(self.file, "a") as file:
            file.write(json.dumps(obj))
            file.write("\n")
        return "Success"


    def read_from_log(self) -> list[str]:
        with open(self.file, "r") as file:
            data = file.readlines()
            return data


    def clear_log(self) -> str:
        with open(self.file, "w") as file:
            file.write("")
        return "Success"


    def get_log_as_json(self) -> list[dict]:
        data = self.read_from_log()
        data = [json.loads(line.replace("\n", "")) for line in data]
        return data


    def get_log_as_dataframe(self) -> pd.DataFrame:
        data = self.get_log_as_json()
        df = pd.DataFrame.from_dict(data, orient='columns')
        return df    