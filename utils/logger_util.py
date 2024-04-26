import logging
import sys

"""   
NOTSET=0
DEBUG=10
INFO=20
WARNING=30
ERROR=40
CRITICAL=50
"""

class Logger_util(): 
    
    
    def __init__(self, log_file: str):
        
        self.log_file = log_file
        self.logger = self.config_logger()
    
    def config_logger(self) -> logging.Logger:        
        
        logger = logging.getLogger(__name__)
        if not logger.hasHandlers():        
        
            logger.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

            stdout_handler = logging.StreamHandler(sys.stdout)
            stdout_handler.setLevel(logging.NOTSET)
            stdout_handler.setFormatter(formatter)

            file_handler = logging.FileHandler(self.log_file)
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)

            logger.addHandler(file_handler)
            logger.addHandler(stdout_handler)
        
        return logger

    def read_log_as_json(self) -> list[dict]:
        
        with open(self.log_file, 'r') as file:
            data = []
            order = ["date", "type", "message"]
            lines = file.readlines()

        for line in lines:
            details = line.split("|")
            details = [x.strip() for x in details]
            structure = {key: value for key, value in zip(order, details)}
            data.append(structure)

        return data