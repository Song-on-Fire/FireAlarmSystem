import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish #publish dependency
from constants import ConfigUtils
import subprocess
import pwa_controller as p_cntr
import sqlite3
import time
from datetime import datetime

def execute_query_with_retry(conn, query:str, values = None, requires_commit=False, max_retries=3, delay = 0.1, executeMany = False ):
    for i in range(max_retries):
        try: 
            cursor = conn.cursor()
            if values and executeMany:
                cursor.executemany(query, values)
            elif values:
                print(values)
                print(query)
                cursor.execute(query, values)
            else:
                cursor.execute(query)
            if requires_commit:
                conn.commit()
            return cursor.fetchall() # if the command does not return rows, then empty list is returned
        except sqlite3.OperationalError as err:
            if "database is locked" in str(err):
                print(f"Database is locked. Retrying in {delay} seconds...")
                time.sleep(delay)
                continue
            else:
                raise
    raise sqlite3.OperationalError("Max retries exceeded. Unable to execute query.")
    conn.close()

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
    utils = ConfigUtils()
    try:
        subprocess.run(['mosquitto_passwd', '-b', utils._BROKER_PASSWD, username, password], check=True)
        utils.reloadConfigFile()
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error from adding {username},{password} to {utils._BROKER_PASSWD}: {e}")

def disconnectSetup():
    utils = ConfigUtils()
    tempClient = mqtt.Client()
    tempClient.username_pw_set(username="default", password="blaze")
    tempClient.connect(utils._HOST, 1883)
    tempClient.disconnect()
    print("Disconnecting unauthorized client")

# TODO: add function to open sqlite database, insert a new row into alarms, commit
def addAlarmToDB(alarmSerial):
    connection = sqlite3.connect("/home/devnico/repos/senior-design/FireAlarmApp/db.sqlite")
    insertQuery = '''INSERT INTO alarms (alarmSerial, createdAt, updatedAt) VALUES (?,?,?)'''
    selectQuery = '''SELECT * FROM alarms WHERE alarmSerial = ?'''
    # check if alarmSerial already exists in DB
    if execute_query_with_retry(conn=connection, query=selectQuery, values=(alarmSerial,)):
        # if rows are returned, return success (True)
        return None
    else:
        execute_query_with_retry(conn=connection,query=insertQuery, values=(alarmSerial,datetime.now(), datetime.now()), requires_commit=True)
        return True
    #
    #  else
        # run Insert query
    pass

def handleSetupMessage(client,msg):
    topic = msg.topic
    payload = msg.payload.decode()
    logMessage(topic, payload)

    # if payload['key'] != consts.ALARM_KEY:
    #     disconnectSetup()
    msgList = payload.split(",") # expect [alarmSerial, username, password]

    if len(msgList) != 3:
        print("incorrect number of parameters, disconnecting now")
        disconnectSetup()
    else:
        if addUsernamePassword(username = msgList[1], password = msgList[2]):
            # if adding the username, password come backs good, then add alarmSerial to DB
            # response = p_cntr.addAlarmToDB(alarmSerial=payload)
            # if(not response):
            #     print("Error")
            # print(response)
            if addAlarmToDB(msgList[0]):
                print(f"alarm serial {msgList[0]}added to DB")
            else:
                print("alarm already exists in DB")
        else:
            print("Error with adding username and password to system")

            
def handleERMessage(client, msg):
    utils = ConfigUtils()
    # extract topic and payload from message
    topic = msg.topic
    payload = msg.payload.decode()
    logMessage(topic, payload)


    # the fire alarm username/id is appended to the topic
    alarmSerial = topic[(topic.rindex("/") + 1): ]

    # get confirmation from PWA, this will send the push notification 
    activeUserConfirmation = p_cntr.getActiveUserConfirmation(alarmID = alarmSerial)
    # alarmID will be stored in topics, username in topic will become deprecated feature

    if (activeUserConfirmation is None) or activeUserConfirmation:
        # if the active user does not respond, notify all alarms with the topic /response/<alarmSerial> 
        # payload = "1"
        sendMessage(client, utils._CONTROLLER_RESPONSE_TOPIC + "/" + alarmSerial, message = "1")
    elif not activeUserConfirmation: 
        sendMessage(client, utils._CONTROLLER_RESPONSE_TOPIC + "/" + alarmSerial, message = "0")

