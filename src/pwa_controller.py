import requests
import configparser

# Define config parser
config = configparser.ConfigParser()
# config file path
CONFIG_FILE_RELPATH = 'config/config.ini'
# Read in config.ini
config.read(CONFIG_FILE_RELPATH)

# CONSTANTS
PWA_NOTIFY_URL = config.get("PWA", "notify_url")
PWA_CONFIRM_URL = config.get("PWA", "confirm_url")
PWA_ADD_ALARM_URL = config.get("PWA", "add_alarm_url")


def notifyActiveUser(alarmID, msgPayload):
    postData = {
    "username": alarmID,
    "notification": {
        "title": "Fire Alarm Emergency", 
        "message": msgPayload.decode()
        }
    }
    response = requests.post(PWA_NOTIFY_URL, json = postData)
    print(response.status_code)
    if response.status_code == 200:
        print("Push Notification Sent Successfully")
    elif response.status_code == 404:
        print("User not found in Users/Subscriptions")
    print(str(response))
        
def getActiveUserConfirmation(alarmID):
    activeUserConfirmation = None
    parameters = {
        "alarmId": alarmID
    }
    response = requests.get(PWA_CONFIRM_URL, params = parameters)
    if response.status_code == 200: 
        activeUserConfirmation = response.confirmed
    else: 
        print("An error occured in confirming the fire status with the active user")
        print(str(response))    
    return activeUserConfirmation

def addUserToAlarm():
    response = requests.post(PWA_ADD_ALARM_URL, json = {})
    if response.status_code == 200: 
        print("Alarm Linked Successfully")
    else: 
        print("An error occurred in linking")
        print(str(response))

def notifyPassiveUser(alarmID, msg):
    pass


