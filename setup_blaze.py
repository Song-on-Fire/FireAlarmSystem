import configparser
import os
import subprocess
# Define config parser
config = configparser.ConfigParser()
# config file path
CONFIG_FILE_RELPATH = 'config/config.ini'
# Read in config.ini
config.read(CONFIG_FILE_RELPATH)
# Define controller root directory
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def writeBrokerFilePaths():
    try:
        subprocess.run("cat " + CONFIG_FILE_RELPATH, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error with reading {CONFIG_FILE_RELPATH}: {e}")
        
    if not config.has_section("BROKER"):
        print("Error: config.ini BROKER section not found")
        exit()

    config.set("BROKER", "password_file", os.path.join(ROOT_DIR, "broker/auth/passwords"))
    config.set("BROKER", "log_dest", os.path.join(ROOT_DIR, "broker/logs/blaze_mosquitto.log"))
    config.set("BROKER", "persistence_location", os.path.join(ROOT_DIR, "broker/storage/"))
    config.set("BROKER", "pid_file", os.path.join(ROOT_DIR, "broker/blaze_mosquitto.pid"))
    with open(CONFIG_FILE_RELPATH, 'a') as config_file:
        config.write(config_file)

    try:
        subprocess.run("cat " + CONFIG_FILE_RELPATH, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error with reading {CONFIG_FILE_RELPATH}: {e}")



def getBrokerConfig():
    broker_config = {}
    if not config.has_section("BROKER"):
        print("Error: config.ini BROKER section not found")
        exit()
    else:
        for key,value in config.items("BROKER"):
            broker_config[key] = value

    return broker_config

def main():
    # Write all root path in config file

    # Write broker file paths in config file

    PWA_PUSH_URL = config.get('PWA', 'push_url')
    # get all broker configurations
    BROKER_CONFIG = getBrokerConfig()




if __name__ == "__main__":

    main()