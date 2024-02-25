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

# BROKER_HOST = "mqtt.eclipseprojects.io"
    
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    if(rc == 5):
        print("Authentication Error on Broker")
        exit()
    print("Connected to Broker with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    MQTTMessage = '{"username": "test", "password": "testPass", "key": "longagothefournationslivedtogetherinharmonytheneverythingchangedwhenthefirenationattacked"}'
    print(f"Sending: {MQTTMessage} to topic /setup")
    client.publish(consts.SETUP_ALARM_TOPIC, payload=MQTTMessage, qos=0)

# The callback for when a PUBLISH message is received from the server.
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
    client.connect(consts.HOST, 1883)

    while True: 
        client.loop()


if __name__ == "__main__":
    main()