import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish #publish dependency
from constants import ConfigUtils
import subprocess
import pwa_controller as p_cntr
import sqlite3
import time
from datetime import datetime
import os
import csv

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
        utils.reloadConfigFileaddAlarm()
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error from adding {username},{password} to {utils._BROKER_PASSWD}: {e}")
    return None

def disconnectSetup():
    utils = ConfigUtils()
    tempClient = mqtt.Client()
    tempClient.username_pw_set(username="default", password="blaze")
    tempClient.connect(utils._HOST, 1883)
    tempClient.disconnect()
    print("Disconnecting unauthorized client")

def addAlarmToDB(alarmSerial):
    # change this path for where the sqlite db is located in the projectserver
    connection = sqlite3.connect("/home/larnell/Blaze-PWA/BlazeFrontEnd/FireAlarmApp/db.sqlite")
    insertQuery = '''INSERT INTO alarms (alarmSerial, location, createdAt, updatedAt) VALUES (?,?,?,?)'''
    selectQuery = '''SELECT * FROM alarms WHERE alarmSerial = ?'''
    # check if alarmSerial already exists in DB
    if execute_query_with_retry(conn=connection, query=selectQuery, values=(alarmSerial,)):
        # if rows are returned, return success (True)
        connection.close()
        return None
    else:
        execute_query_with_retry(conn=connection,query=insertQuery, values=(alarmSerial,"unknown", datetime.now(), datetime.now()), requires_commit=True)
        connection.close()
        return True
    #
    #  else
        # run Insert query

def getAllAlarmsInDB():
    selectQuery = '''SELECT alarmSerial FROM alarms'''
    connection = sqlite3.connect("/home/larnell/Blaze-PWA/BlazeFrontEnd/FireAlarmApp/db.sqlite")
    alarm_rows = execute_query_with_retry(conn=connection, query=selectQuery)
    return alarm_rows

def sendMessageToAlarms(client, allAlarms, topic, message):
    for alarmSerial in allAlarms:
        sendMessage(client, topic+alarmSerial, message)


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
    event = str()

    # the fire alarm username/id is appended to the topic
    alarmSerial = topic[(topic.rindex("/") + 1): ]

    # get confirmation from PWA, this will send the push notification 
    activeUserConfirmation = p_cntr.getActiveUserConfirmation(alarmID = alarmSerial)
    # alarmID will be stored in topics, username in topic will become deprecated feature
    utils.setResponseLogTime()
    if (activeUserConfirmation["confirmed"] is None) or activeUserConfirmation["confirmed"] == True:
        # if the active user does not respond, notify all alarms with the topic /response/<alarmSerial> 
        allAlarms = getAllAlarmsInDB()
        sendMessageToAlarms(client, allAlarms, utils._CONTROLLER_RESPONSE_TOPIC + "/", message = "1")
        #sendMessage(client, utils._CONTROLLER_RESPONSE_TOPIC + "/" + alarmSerial, message = "1")
        # Notify all passive users
        p_cntr.notifyPassiveUser(activeUserConfirmation)
        event = "True Alarm.All Users Notified"
    else: 

        sendMessage(client, utils._CONTROLLER_RESPONSE_TOPIC + "/" + alarmSerial, message = "0")
        event = "False Alarm"
    writeToLog(location = activeUserConfirmation["location"], response = event)

def writeToLog(location, response):
    utils = ConfigUtils()
    departmentLogPath = os.path.join(utils._ROOT_DIR, "departmentLog/alarmsLog.csv")
    data = [utils._receive_msg_time, location, utils._receive_response_time, response]
    with open(departmentLogPath, 'a', newline='') as file:
        writer = csv.writer(file)
        # Append the data to the csv file
        writer.writerow(data)
    
