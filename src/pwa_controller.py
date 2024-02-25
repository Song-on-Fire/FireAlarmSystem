import requests
import constants as consts
import random 
import string

def notifyActiveUser(alarmID, msgPayload):
    postData = {
    "username": alarmID,
    "notification": {
        "title": "Fire Alarm Emergency", 
        "message": msgPayload
        }
    }
    response = requests.post(consts.PWA_NOTIFY_URL, json = postData) # /notify
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
    response = requests.get(consts.PWA_CONFIRM_URL, params = parameters) # /confirm 
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
    response = requests.post(consts.PWA_ADD_ALARM_URL, json = {})
    if response.status_code == 200: 
        print("Alarm Linked Successfully")
    else: 
        print("An error occurred in linking")
    print(str(response))

def addAlarmToDB():
    print("adding alarm to the PWA database")
    # Send API request to PWA, response should contain alarmSerial
    
    # simulating random alarmSerial ID

    source = string.ascii_letters + string.digits
    alarmSerial = ''.join((random.choice(source) for i in range(10)))
    return alarmSerial

def notifyPassiveUser(alarmID, msg):
    pass


