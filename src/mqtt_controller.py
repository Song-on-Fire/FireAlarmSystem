import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish #publish dependency
import configparser

# Define config parser
config = configparser.ConfigParser()
# config file path
CONFIG_FILE_RELPATH = 'config/config.ini'
# Read in config.ini
config.read(CONFIG_FILE_RELPATH)

# Constants
FIRE_ALARM_ER_TOPIC = config.get("TOPICS", "emergency_alarm")
FIRE_ALARM_RESPONSE_TOPIC = config.get("TOPICS", "controller_response")

def subscribeToERMessages(client):
    client.subscribe(FIRE_ALARM_ER_TOPIC)


def handleERMessage(client, msg):
    pass

def sendFalseAlarmMessage(alarmID):
    pass 

def sendTrueAlarmMessage(alarmID):
    pass
