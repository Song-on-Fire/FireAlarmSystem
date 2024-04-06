import requests
from constants import ConfigUtils
import random 
import string
import time

utils = ConfigUtils()

def notifyActiveUser(alarmID, msgPayload):
    postData = {
    "username": alarmID,
    "notification": {
        "title": "Fire Alarm Emergency", 
        "message": msgPayload
        }
    }
    response = requests.post(utils._PWA_NOTIFY_URL, json = postData) # /notify
    print(response.status_code)
    if response.status_code == 200:
        print("Push Notification Sent Successfully")
    elif response.status_code == 404:
        print("User not found in Users/Subscriptions")
    print(str(response))
        

def getActiveUserConfirmation(alarmID):
    utils = ConfigUtils()
    activeUserConfirmation = dict()
    parameters = {
        "&timestamp": time.mktime(utils._receive_msg_time.timetuple()),
        "alarmId": alarmID # 
    }
    response = requests.get(utils._PWA_CONFIRM_URL, params = parameters) # /confirm 
    result = response.json()
    if response.status_code == 200: 
        print("Successfully received PWA response")
        activeUserConfirmation["confirmed"] = result["confirmed"]
        activeUserConfirmation["location"] = result["location"]
    else: 
        print("An error occured in confirming the fire status with the active user")
    print(result) 
    if activeUserConfirmation["confirmed"] == 'null':
        activeUserConfirmation["confirmed"] = None
    return activeUserConfirmation

def linkUserToAlarm():
    response = requests.post(utils._PWA_ADD_ALARM_URL, json = {})
    if response.status_code == 200: 
        print("Alarm Linked Successfully")
    else: 
        print("An error occurred in linking")
    print(str(response))

# def addAlarmToDB(alarmSerial):
#     print("adding alarm to the PWA database")
#     # Send API request to PWA to add a fire alarm to the DB with alarmSerial = alarmSerial
    
#     response = "{response}"
#     return response

def notifyPassiveUser(alarmLocation):
    # TODO: need API to notify all passive users
    msg = f"Fire located at {alarmLocation}"
    requestBody = {
        "&timestamp": time.mktime(utils._receive_msg_time.timetuple()),
        "notification": {
            "title": "Fire Detected!",
            "message": msg
        }
    }
    response = requests.post(utils._PWA_NOTIFY_URL, params = requestBody) # /confirm 
    result = response.json()
    if response.status_code == 200: 
        print("response code 200")
    else: 
        print("An error occured in sending the push notification")
    print(response)


