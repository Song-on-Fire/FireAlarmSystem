import configparser
import os
import subprocess
import time # for testing
import sys
sys.path.append('src/')
from blaze_client import run_client
from constants import ConfigUtils

utils = ConfigUtils()
# Define controller root directory
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
#mosquitto
CONFIG_FILE_PATH = os.path.join(ROOT_DIR, "config/config.ini")

def writeMosquittoFilePaths():
    if not utils._config.has_section("MOSQUITTO"):
        print("Error: utils._config.ini BROKER section not found")
        sys.exit()

    # Auth File Paths
    utils._config.set("MOSQUITTO", "password_file", os.path.join(ROOT_DIR, "broker/auth/passwords"))
    utils._config.set("MOSQUITTO", "acl_file", os.path.join(ROOT_DIR, "broker/auth/blaze_aclfile"))
    # Log File Path
    utils._config.set("MOSQUITTO", "log_dest", "file " + os.path.join(ROOT_DIR, "broker/logs/blaze_mosquitto.log"))

    # Mosquitto Broker DB
    utils._config.set("MOSQUITTO", "persistence_location", os.path.join(ROOT_DIR, "broker/storage/"))
    
    # Mosquitto Broker Pid File
    utils._config.set("MOSQUITTO", "pid_file", os.path.join(ROOT_DIR, "broker/blaze_mosquitto.pid"))
    with open(CONFIG_FILE_PATH, 'w') as config_file:
        utils._config.write(config_file)

def writeProjectFilePaths():

    if not utils._config.has_section("PATHS"):
        utils._config.add_section("PATHS")

    utils._config.set("PATHS", "root_dir", ROOT_DIR)
    utils._config.set("PATHS", "mosquitto_config_file", os.path.join(ROOT_DIR, "broker/blaze_mosquitto_utils._config.conf"))

    with open(CONFIG_FILE_PATH, 'w') as config_file:
        utils._config.write(config_file)

def getMosquittoConfig():
    broker_config = {}
    if not utils._config.has_section("MOSQUITTO"):
        print("Error: utils._config.ini MOSQUITTO section not found")
        exit()
    else:
        for key,value in utils._config.items("MOSQUITTO"):
            broker_config[key] = value

    return broker_config

def createMosquittoConfiguration(config_dict):
    line_content = ""
    blaze_mosquitto_config_location = os.path.join(ROOT_DIR, "broker/blaze_mosquitto_utils._config.conf")
    with open(blaze_mosquitto_config_location, 'w') as file:
        for key,value in config_dict.items():
            line_content = f"{key} {value}\n"
            file.write(line_content)

def startMosquittoService():
    command = "mosquitto -v -d -c " + utils._config.get("PATHS", "mosquitto_config_file")
    try:
        print(command)
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error with reading {CONFIG_FILE_PATH}: {e}")
    
def mosquitto_is_running():
    try: 
        result = subprocess.run(['systemctl', 'is-active', 'mosquitto'], check=True, capture_output=True, text=True)
        if result == "active":
            print("mosquitto is already running")
            return True
        elif result == "inactive":
            print("mosquitto is not running")
            return False
    except subprocess.CalledProcessError as e:
        print(f"There was an error while checking mosquitto was active: {e}")
        sys.exit()
    
def main(): 
    utils._config.read(CONFIG_FILE_PATH)
    # Write all project paths in config file
    writeProjectFilePaths()
    # Write mosquitto file paths in config file
    writeMosquittoFilePaths()
    # Set up programatic constants
    utils.setUpConfigFileVars(file_path=CONFIG_FILE_PATH)
    # get all mosquitto configurations
    MOSQUITTO_CONFIG = getMosquittoConfig()
    # write them to blaze mosquitto conf file
    createMosquittoConfiguration(MOSQUITTO_CONFIG)
    # run Mosquitto Service
    if mosquitto_is_running():
        print("Service is running. Reloading config.")
        utils.reloadConfigFile()
    else:
        startMosquittoService()

    run_client()


if __name__ == "__main__":

    main()