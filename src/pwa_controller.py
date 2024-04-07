import requests
from constants import ConfigUtils
import time

utils = ConfigUtils()

def getActiveUserConfirmation(alarmID):
    activeUserConfirmation = dict()
    parameters = {
        "&timestamp": time.mktime(utils._receive_msg_time.timetuple()),
        "alarmId": alarmID # 
    }
    authHeader = {"authorization": utils._AUTH_TOKEN}
    response = requests.get(utils._PWA_CONFIRM_URL, params = parameters, headers=authHeader) # /confirm 
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

def notifyPassiveUser(alarmLocation):
    msg = f"Fire located at {alarmLocation}"
    requestBody = {
        "&timestamp": time.mktime(utils._receive_msg_time.timetuple()),
        "notification": {
            "title": "Fire Detected!",
            "message": msg
        }
    }
    authHeader = {"authorization": utils._AUTH_TOKEN}
    response = requests.post(utils._PWA_NOTIFY_URL, params = requestBody, headers=authHeader) # /confirm 
    result = response.json()
    if response.status_code == 200: 
        print("response code 200")
    else: 
        print("An error occured in sending the push notification")
    print(response)


