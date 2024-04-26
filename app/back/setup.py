from configparser import ConfigParser
import os.path


def read_config():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    config_filepath = dir_path+"/config.ini"
    # check if the config file exists
    exists = os.path.exists(config_filepath)
    config = None
    if exists:
        print("--------config.ini file found at ", config_filepath)
        config = ConfigParser()
        config.read(config_filepath)
    else:
        print("---------config.ini file not found at ", config_filepath)
    return config

# Retrieve config details
#log_config = config["LOG"]
#print(log_config["file"])