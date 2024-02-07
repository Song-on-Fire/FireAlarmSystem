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
FIRE_ALARM_ER_PREFIX = config.get("TOPICS", "emergency_alarm")
FIRE_ALARM_ER_TOPIC = FIRE_ALARM_ER_PREFIX + "/#"
PWA_NOTIFY_URL = config.get("PWA", "notify_url")
HOST = config.get("PWA", "host")

# BROKER_HOST = "mqtt.eclipseprojects.io"

# TODO: Move message logging into mqtt-controller

# The callback for when the client receives a CONNACK response from the broker.
def on_connect(client, userdata, flags, rc):

    if(rc == 5):
        print("Authentication Error on Broker")
        exit()
    print("Connected with result code "+str(rc))

    # subscribe controller client to all ER messages
    m_cntr.subscribeToERMessages(client)
    # link test user and fire alarm in PWA db
    p_cntr.addUserToAlarm()

# Callback when controller receives a message from the broker
def on_message(client, userdata, msg):
    topic = msg.topic
    if topic.startswith(FIRE_ALARM_ER_PREFIX): 
        m_cntr.handleERMessage(client, msg)   

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
