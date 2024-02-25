import configparser
# Define config parser
config = configparser.ConfigParser()
# config file path
CONFIG_FILE_RELPATH = '../config/config.ini'
# Read in config.ini
config.read(CONFIG_FILE_RELPATH)

# topics
CONFIG_ALARM_TOPIC = config.get("TOPICS", "config_alarm")
SETUP_ALARM_TOPIC = config.get("TOPICS", "setup_alarm")
FIRE_ALARM_ER_TOPIC = config.get("TOPICS", "emergency_alarm")
CONTROLLER_RESPONSE_TOPIC = config.get("TOPICS", "controller_response")
# API urls
PWA_NOTIFY_URL = config.get("PWA", "notify_url")

# server host
HOST = config.get("PWA", "host")

# blaze client credentials
CLIENT_USERNAME = "admin"
CLIENT_PASSWORD = "songisonfire"