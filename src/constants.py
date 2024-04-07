import configparser
import subprocess
from datetime import datetime

class ConfigUtils:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self):
        self._config = configparser.ConfigParser()

    def setUpConfigFileVars(self, file_path):
        self._CONFIG_FILE_PATH = file_path
        self._config.read(self._CONFIG_FILE_PATH)
        # topics
        #self._CONFIG_ALARM_TOPIC = self._config.get("TOPICS", "config_alarm") + "/#"
        self._SETUP_ALARM_TOPIC = self._config.get("TOPICS", "setup_alarm")
        self._FIRE_ALARM_ER_TOPIC = self._config.get("TOPICS", "emergency_alarm") + "/#"
        self._CONTROLLER_RESPONSE_TOPIC = self._config.get("TOPICS", "controller_response")
        
        # PWA APIs
        self._PWA_NOTIFY_URL = self._config.get("PWA", "notify_url")
        self._PWA_CONFIRM_URL = self._config.get("PWA", "confirm_url")
        self._PWA_ADD_ALARM_URL = self._config.get("PWA", "add_alarm_url") 
        self._HOST = self._config.get("PWA", "host")

        # Credentials
        #self._ALARM_KEY = self._config.get("KEYS", "alarm_key")
        self._CLIENT_USERNAME = self._config.get("KEYS", "client_username")
        self._CLIENT_PASSWORD = self._config.get("KEYS", "client_password")
        self._AUTH_TOKEN = self._config.get("KEYS", "auth_token")

        # Important Paths
        self._BROKER_PID_FILEPATH = self._config.get("MOSQUITTO", "pid_file")
        self._BROKER_PASSWD = self._config.get("MOSQUITTO", "password_file")
        self._ROOT_DIR = self._config.get("PATHS", "root_dir")

        # Broker IP
        self._BROKER_IP = self._config.get("MOSQUITTO", "bind_address")
    
    def reloadConfigFile(self):
        try:
            subprocess.run(["kill","-SIGHUP", "$(cat ", self._BROKER_PID_FILEPATH, ")"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error with reloading mosquitto config file: {e}")
        
    def setMsgLogTime(self):
        self._receive_msg_time = datetime.now()
    
    def setResponseLogTime(self):
        self._receive_response_time = datetime.now()

