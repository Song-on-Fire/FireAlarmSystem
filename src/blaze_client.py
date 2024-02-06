import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish #publish dependency
import requests # to send API request to PWA
import configparser
import mqtt_controller as m_cntr
import pwa_controller as p_cntr

# Define config parser
config = configparser.ConfigParser()
# config file path
CONFIG_FILE_RELPATH = 'config/config.ini'
# Read in config.ini
config.read(CONFIG_FILE_RELPATH)

# Constants
CLIENT_USERNAME = "nebokha"
CLIENT_PASSWORD = "password"
FIRE_ALARM_USERNAME = "bcsotty"
FIRE_ALARM_ER_TOPIC = config.get("TOPICS", "emergency_alarm") + "/" + FIRE_ALARM_USERNAME
PWA_PUSH_URL = config.get("PWA", "push_url")
HOST = config.get("PWA", "host")

# BROKER_HOST = "mqtt.eclipseprojects.io"

# TODO: Move message logging into mqtt-controller

# The callback for when the client receives a CONNACK response from the broker.
def on_connect(client, userdata, flags, rc):

    # print("Connected to Broker. Result Code: "+str(rc))
    if(rc == 5):
        print("Authentication Error on Broker")
        exit()
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # subscribing to FireAlarm topic

    # TODO: create function to subscribe to necessary topics for the client
    m_cntr.subscribeToERMessages(client)

# The callback for when a message is published to the broker, and the backendreceives it
def on_message(client, userdata, msg):
    payload = str(msg.payload)
    topic = msg.topic

    # TODO: Logic that parses topic for which mqtt-controller handler to call
    # Print MQTT message to console
    print("From Topic: " + topic)
    print("Received: " + payload)
    usernameStart = (topic.rindex("/") + 1)
    print(f"Index of username: {usernameStart}" )
    username = topic[usernameStart:]
    print(username)
    # TODO: Post Request handled by pwa_controller, 
    # Create Body for POST to PWA 
        # sub: Push Notification Subscription
        # notification: Contains fields that appear on native push notification
    
    p_cntr.notifyActiveUser()
    data = {
    "username": username,
    "notification": {
        "title": "Fire Alarm Emergency", 
        "message": msg.payload.decode()
        }
    }   
    # Post data to PWA hosted at URL
    response = requests.post(PWA_PUSH_URL, json = data)
    print(response.status_code)
    if response:
        print(str(response))
    else:
        print("An error occured with the response") 

def run_client():

    # create MQTT Client
    client = mqtt.Client()
    # Set Paho API functions to our defined functions
    client.on_connect = on_connect
    client.on_message = on_message
    # Set username and password 
    client.username_pw_set(username=CLIENT_USERNAME, password=CLIENT_PASSWORD)
    # Connect client to the Broker
    client.connect(HOST, 1883)

    # Run cliet forever
    while True:
        client.loop()

if __name__ == "__main__":
    run_client()
