import configparser
import os
import subprocess
import time # for testing
import sys
sys.path.append('src/')
from blaze_client import run_client

# Define config parser
config = configparser.ConfigParser()
# config file path
CONFIG_FILE_RELPATH = 'config/config.ini'
# Read in config.ini
config.read(CONFIG_FILE_RELPATH)
# Define controller root directory
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
#mosquitto

def writeMosquittoFilePaths():

    if not config.has_section("MOSQUITTO"):
        print("Error: config.ini BROKER section not found")
        exit()

    config.set("MOSQUITTO", "password_file", os.path.join(ROOT_DIR, "broker/auth/passwords"))
    config.set("MOSQUITTO", "log_dest", "file " + os.path.join(ROOT_DIR, "broker/logs/blaze_mosquitto.log"))
    config.set("MOSQUITTO", "persistence_location", os.path.join(ROOT_DIR, "broker/storage/"))
    config.set("MOSQUITTO", "pid_file", os.path.join(ROOT_DIR, "broker/blaze_mosquitto.pid"))
    with open(CONFIG_FILE_RELPATH, 'w') as config_file:
        config.write(config_file)

def writeProjectFilePaths():

    if not config.has_section("PATHS"):
        config.add_section("PATHS")

    config.set("PATHS", "root_dir", ROOT_DIR)
    config.set("PATHS", "mosquitto_config_file", os.path.join(ROOT_DIR, "broker/blaze_mosquitto_config.conf"))

    with open(CONFIG_FILE_RELPATH, 'w') as config_file:
        config.write(config_file)



def getMosquittoConfig():
    broker_config = {}
    if not config.has_section("MOSQUITTO"):
        print("Error: config.ini MOSQUITTO section not found")
        exit()
    else:
        for key,value in config.items("MOSQUITTO"):
            broker_config[key] = value

    return broker_config

def createMosquittoConfiguration(config_dict):
    line_content = ""
    blaze_mosquitto_config_location = os.path.join(ROOT_DIR, "broker/blaze_mosquitto_config.conf")
    with open(blaze_mosquitto_config_location, 'w') as file:
        for key,value in config_dict.items():
            line_content = f"{key} {value}\n"
            file.write(line_content)

def startMosquittoService():
    command = "mosquitto -v -d -c " + config.get("PATHS", "mosquitto_config_file")
    try:
        print(command)
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error with reading {CONFIG_FILE_RELPATH}: {e}")
    
def mosquitto_is_running():
    try: 
        subprocess.run(['systemctl', 'is-active', 'mosquitto'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False
    
def main(): 
    # Write all project paths in config file
    writeProjectFilePaths()
    # Write mosquitto file paths in config file
    writeMosquittoFilePaths()
    # get all mosquitto configurations
    MOSQUITTO_CONFIG = getMosquittoConfig()
    # write them to blaze mosquitto conf file
    createMosquittoConfiguration(MOSQUITTO_CONFIG)
    # run Mosquitto Service
    if mosquitto_is_running():
        print("Service is running. Please reload the config file.")
        exit()
    else:
        startMosquittoService()

    run_client()


if __name__ == "__main__":

    main()