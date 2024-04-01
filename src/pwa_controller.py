import requests
from constants import ConfigUtils
import random 
import string

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
    activeUserConfirmation = None
    parameters = {
        "alarmId": alarmID # 
    }
    response = requests.get(utils._PWA_CONFIRM_URL, params = parameters) # /confirm 
    result = response.json()
    if response.status_code == 200: 
        print("Successfully received PWA response")
        activeUserConfirmation = result["confirmed"]
    else: 
        print("An error occured in confirming the fire status with the active user")
    print(result) 
    if activeUserConfirmation == 'null':
        activeUserConfirmation = None
    return activeUserConfirmation

def linkUserToAlarm():
    response = requests.post(utils._PWA_ADD_ALARM_URL, json = {})
    if response.status_code == 200: 
        print("Alarm Linked Successfully")
    else: 
        print("An error occurred in linking")
    print(str(response))

def addAlarmToDB(alarmSerial):
    # TODO: Add sqlite db adding alarm to DB
    print("adding alarm to the PWA database")
    # Send API request to PWA to add a fire alarm to the DB with alarmSerial = alarmSerial
    
    response = "{response}"
    return response

def notifyPassiveUser(alarmID, msg):
    pass


