import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish #publish dependency
import configparser
import pwa_controller as p_cntr

# Define config parser
config = configparser.ConfigParser()
# config file path
CONFIG_FILE_RELPATH = 'config/config.ini'
# Read in config.ini
config.read(CONFIG_FILE_RELPATH)

# Constants
CLIENT_USERNAME = "nebokha"
CLIENT_PASSWORD = "password"
FIRE_ALARM_ER_PREFIX = config.get("TOPICS", "emergency_alarm")
FIRE_ALARM_ER_TOPIC = FIRE_ALARM_ER_PREFIX + "/#"
FIRE_ALARM_RESPONSE_PREFIX = config.get("TOPICS", "controller_response")
HOST = config.get("PWA", "host")


def subscribeToERMessages(client):
    client.subscribe(FIRE_ALARM_ER_TOPIC)


def handleERMessage(client, msg):
    # extract topic and payload from message
    topic = msg.topic
    payload = msg.payload.decode()
    print("Topic:" + topic)
    print("Payload: " + payload)
    print("")

    # the fire alarm username/id is appended to the topci
    username = topic[(topic.rindex("/") + 1): ]

    # have PWA controller send push notification   
    # p_cntr.notifyActiveUser(alarmID=username, msgPayload=payload) # /notify will become deprecated internal function soon 

    # get confirmation from PWA, this will send the push notification 
    activeUserConfirmation = p_cntr.getActiveUserConfirmation(alarmID = 1) # get /confirm 
    print(activeUserConfirmation)
    if (activeUserConfirmation is None) or activeUserConfirmation:
        sendTrueAlarmMessage(username)
    elif not activeUserConfirmation:
        sendFalseAlarmMessage(username, client)
    
def sendFalseAlarmMessage(alarmID, client):
    MQTTMessage = "0"
    client.publish("/response/bcsotty", payload=MQTTMessage, qos=0)
    publish.single(FIRE_ALARM_RESPONSE_PREFIX + "/" + alarmID, MQTTMessage, hostname = HOST, auth={'username':CLIENT_USERNAME, 'password':CLIENT_PASSWORD})

def sendTrueAlarmMessage(alarmID):
    MQTTMessage = "1"
    publish.single(FIRE_ALARM_RESPONSE_PREFIX + "/" + alarmID, MQTTMessage, hostname = HOST, auth={'username':CLIENT_USERNAME, 'password':CLIENT_PASSWORD})
