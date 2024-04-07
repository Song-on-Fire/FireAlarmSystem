import paho.mqtt.client as mqtt
from constants import ConfigUtils
import subprocess
import pwa_controller as p_cntr
import db_controller as db_cntr
import os
import csv

utils = ConfigUtils()

def subscribeToTopics(topics: tuple, client):
    for topic in topics:
        print(f"Blaze Client Subscribing to {topic}")
        client.subscribe(topic)

def logMessage(topic, payload):
    print(f"topic: {topic}")
    print(f"payload: {payload}")

def sendMessage(client, topic, message):
    client.publish(topic, payload = message)

def addUsernamePassword(username, password):
    try:
        subprocess.run(['mosquitto_passwd', '-b', utils._BROKER_PASSWD, username, password], check=True)
        utils.reloadConfigFilea()
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error from adding {username},{password} to {utils._BROKER_PASSWD}: {e}")
    return None

def disconnectSetup():
    tempClient = mqtt.Client()
    tempClient.username_pw_set(username="default", password="blaze")
    tempClient.connect(utils._HOST, 1883)
    tempClient.disconnect()
    print("Disconnecting unauthorized client")


def sendMessageToAlarms(client, allAlarms, topic, message):
    for alarmSerial in allAlarms:
        sendMessage(client, topic+alarmSerial, message)


def handleSetupMessage(client,msg):
    topic = msg.topic
    payload = msg.payload.decode()
    logMessage(topic, payload)
    
    msgList = payload.split(",") # expect [alarmSerial, username, password]

    if len(msgList) != 3:
        print("incorrect number of parameters, disconnecting now")
        disconnectSetup()
    else:
        if addUsernamePassword(username = msgList[1], password = msgList[2]):
            if db_cntr.addAlarmToDB(msgList[0]):
                print(f"alarm serial {msgList[0]} added to DB")
            else:
                print("alarm already exists in DB")
        else:
            print("Error with adding username and password to system")

            
def handleERMessage(client, msg):
    # extract topic and payload from message
    topic = msg.topic
    payload = msg.payload.decode()
    logMessage(topic, payload)
    event = str()

    # the fire alarm username/id is appended to the topic
    alarmSerial = topic[(topic.rindex("/") + 1): ]

    # get confirmation from PWA, this will send the push notification 
    activeUserConfirmation = p_cntr.getActiveUserConfirmation(alarmID = alarmSerial)
    # alarmID will be stored in topics, username in topic will become deprecated feature
    utils.setResponseLogTime()

    if (activeUserConfirmation["confirmed"] is None) or activeUserConfirmation["confirmed"] == True:
        # if the active user does not respond, notify all alarms with the topic /response/<alarmSerial> 
        allAlarms = db_cntr.getAllAlarmsInDB()
        sendMessageToAlarms(client, allAlarms, utils._CONTROLLER_RESPONSE_TOPIC + "/", message = "1")
        # Notify all passive users
        p_cntr.notifyPassiveUser(activeUserConfirmation)
        event = "True Alarm.All Users Notified"
    else: 
        sendMessage(client, utils._CONTROLLER_RESPONSE_TOPIC + "/" + alarmSerial, message = "0")
        event = "False Alarm"
    writeToLog(location = activeUserConfirmation["location"], response = event)

def writeToLog(location, response):
    departmentLogPath = os.path.join(utils._ROOT_DIR, "departmentLog/alarmsLog.csv")
    data = [utils._receive_msg_time, location, utils._receive_response_time, response]
    with open(departmentLogPath, 'a', newline='') as file:
        writer = csv.writer(file)
        # Append the data to the csv file
        writer.writerow(data)
    
