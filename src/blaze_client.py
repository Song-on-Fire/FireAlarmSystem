import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish #publish dependency
import requests # to send API request to PWA
from constants import ConfigUtils
import configparser
import mqtt_controller as m_cntr

utils = ConfigUtils()
# BROKER_HOST = "mqtt.eclipseprojects.io"

# The callback for when the client receives a CONNACK response from the broker.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    if(rc == 5):
        print("Authentication Error on Broker")
        exit()
    topics = (
        utils._FIRE_ALARM_ER_TOPIC,
        utils._SETUP_ALARM_TOPIC
    )
    # subscribe controller client to necessary topics
    m_cntr.subscribeToTopics(topics, client)

# Callback when controller receives a message from the broker
def on_message(client, userdata, msg):
    topic = msg.topic
    if mqtt.topic_matches_sub(utils._FIRE_ALARM_ER_TOPIC, topic):
        m_cntr.handleERMessage(client, msg)
    elif mqtt.topic_matches_sub(utils._SETUP_ALARM_TOPIC, topic):
        m_cntr.handleSetupMessage(client, msg)

def run_client():

    # create MQTT Client
    client = mqtt.Client()
    # Set Paho API functions to our defined functions
    client.on_connect = on_connect
    client.on_message = on_message
    # Set username and password 
    client.username_pw_set(username=utils._CLIENT_USERNAME, password=utils._CLIENT_PASSWORD )
    # Connect client to the Broker 
    client.connect(utils._HOST, 1883)

    # Run cliet forever
    while True:
        client.loop()

if __name__ == "__main__":
    run_client()
