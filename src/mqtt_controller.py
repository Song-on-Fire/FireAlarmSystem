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
FIRE_ALARM_ER_TOPIC = config.get("TOPICS", "emergency_alarm") + "/#"
FIRE_ALARM_RESPONSE_TOPIC = config.get("TOPICS", "controller_response")

def subscribeToERMessages(client):
    client.subscribe(FIRE_ALARM_ER_TOPIC)


def handleERMessage(client, msg):
    # extract topic and payload from message
    topic = msg.topic
    payload = str(msg.payload)
    print("Topic:" + topic)
    print("Payload: " + payload)
    print("")

    # the fire alarm username/id is appended to the topci
    username = topic[(topic.rindex("/") + 1): ]

    # Link alarm to user in PWA
    p_cntr.addUserToAlarm()

    # have PWA controller send push notification   
    p_cntr.notifyActiveUser(alarmID=username, msgPayload=payload)

    # get confirmation from PWA
    activeUserConfirmation = p_cntr.getActiveUserConfirmation(alarmID = username)

    print(activeUserConfirmation)



def sendFalseAlarmMessage(alarmID):
    pass 

def sendTrueAlarmMessage(alarmID):
    pass
