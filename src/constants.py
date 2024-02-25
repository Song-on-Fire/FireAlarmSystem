import configparser
# Define config parser
config = configparser.ConfigParser()
# config file path
CONFIG_FILE_RELPATH = '../config/config.ini'
# Read in config.ini
config.read(CONFIG_FILE_RELPATH)

# topics
CONFIG_ALARM_TOPIC = config.get("TOPICS", "config_alarm") + "/#"
SETUP_ALARM_TOPIC = config.get("TOPICS", "setup_alarm")
FIRE_ALARM_ER_TOPIC = config.get("TOPICS", "emergency_alarm") + "/#"
CONTROLLER_RESPONSE_TOPIC = config.get("TOPICS", "controller_response")
# API urls
PWA_NOTIFY_URL = config.get("PWA", "notify_url")
PWA_CONFIRM_URL = config.get("PWA", "confirm_url")
PWA_ADD_ALARM_URL = config.get("PWA", "add_alarm_url")
# server host
HOST = config.get("PWA", "host")

# Credentials
ALARM_KEY = config.get("KEYS", "alarm_key")
CLIENT_USERNAME = config.get("KEYS", "client_username")
CLIENT_PASSWORD = config.get("KEYS", "client_password")