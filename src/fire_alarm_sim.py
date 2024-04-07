# Simulates the Smart Fire Alarm that sends an MQTT Message 
# to the Backend when a Fire is detected
 
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish # publish dependency
import time # for testing
import constants as consts
import configparser

# Define config parser
config = configparser.ConfigParser()
# config file path
CONFIG_FILE_RELPATH = '../config/config.ini'
# Read in config.ini
config.read(CONFIG_FILE_RELPATH)

# Constants
SETUP_USERNAME = "default"
SETUP_PASSWORD = "blaze"
REAL_USERNAME = "bcsotty"
REAL_PASSWORD = "correct"
ALARM_SERIAL = "serial"
real_connect = False


# BROKER_HOST = "mqtt.eclipseprojects.io"
    
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    if(rc == 5):
        print("Authentication Error on Broker")
        exit()
    print("Connected to Broker with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    
    if not real_connect:
        changeConnect(client)
        time.sleep(3)

# The callback for when a PUBLISH message is received from the server.
def changeConnect(client):
    MQTTMessage = ",".join([ALARM_SERIAL, REAL_USERNAME, REAL_PASSWORD])
    print(f"Sending: {MQTTMessage} to topic /setup")
    client.publish("/setup", payload=MQTTMessage, qos=0)
    real_connect = True

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload.decode()))
    time.sleep(5)

def on_disconnect(client, userdata,  reason_code):
    print("disconnected")
    exit()

def main():

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    # Set Username and Password
    client.username_pw_set(username=SETUP_USERNAME, password=SETUP_PASSWORD)
    # Connect to broker
    print(SETUP_USERNAME, SETUP_PASSWORD)
    client.connect("141.215.80.233", 1883)
    while not real_connect: 
        client.loop()
        print("after real connect")
    time.sleep(3)
    client.username_pw_set(username=REAL_USERNAME, password=SETUP_PASSWORD)
    client.connect("141.215.80.233", 1883)
    print("outside first while")
    client.connect("141.215.80.233", 1883)
    while real_connect:
        client.loop()
        print("in real loop")
        time.sleep(5)



if __name__ == "__main__":
    main()