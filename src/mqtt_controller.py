import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish #publish dependency
import constants as consts
import json
import pwa_controller as p_cntr

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
    print(f"username: {username}")
    print(f"password: {password}")
    pass

def disconnectSetup():
    tempClient = mqtt.Client()
    tempClient.username_pw_set(username="default", password="blaze")
    tempClient.connect(consts.HOST, 1883)
    tempClient.disconnect()
    print("Disconnecting unauthorized client")
    pass

def handleSetupMessage(client,msg):
    topic = msg.topic
    payload = msg.payload.decode()
    payload = json.loads(payload)
    logMessage(topic, payload)
    if payload['key'] != consts.ALARM_KEY:
        disconnectSetup()
    addUsernamePassword(payload['username'], payload['password'])
    response = p_cntr.addAlarmToDB()
    print(response)


def handleConfigMessage(client, msg):
    pass

def handleERMessage(client, msg):
    # extract topic and payload from message
    topic = msg.topic
    payload = msg.payload.decode()
    logMessage(topic, payload)


    # the fire alarm username/id is appended to the topic
    username = topic[(topic.rindex("/") + 1): ]

    # get confirmation from PWA, this will send the push notification 
    activeUserConfirmation = p_cntr.getActiveUserConfirmation(alarmID = 1)
    # alarmID will be stored in topics, username in topic will become deprecated feature

    if (activeUserConfirmation is None) or activeUserConfirmation:
        # if the active user does not respond, notify all alarms with the topic /response/<alarmSerial> 
        # payload = "1"
        sendMessage(client, consts.CONTROLLER_RESPONSE_TOPIC + "/" + username, message = "1")
    elif not activeUserConfirmation: 
        sendMessage(client, consts.CONTROLLER_RESPONSE_TOPIC + "/" + username, message = "0")

