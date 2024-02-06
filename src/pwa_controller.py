import requests
import configparser

# Define config parser
config = configparser.ConfigParser()
# config file path
CONFIG_FILE_RELPATH = 'config/config.ini'
# Read in config.ini
config.read(CONFIG_FILE_RELPATH)

# CONSTANTS
PWA_PUSH_URL = config.get("PWA", "push_url")

def notifyActiveUser(alarmID, msg):
    pass

def notifyPassiveUser(alarmID, msg):
    pass


