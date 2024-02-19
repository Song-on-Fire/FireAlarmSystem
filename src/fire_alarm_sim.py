# Simulates the Smart Fire Alarm that sends an MQTT Message 
# to the Backend when a Fire is detected
 
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish # publish dependency
import time # for testing
import configparser

# Define config parser
config = configparser.ConfigParser()
# config file path
CONFIG_FILE_RELPATH = '../config/config.ini'
# Read in config.ini
config.read(CONFIG_FILE_RELPATH)

# Constants
BROKER_HOST = "141.215.80.233"
CLIENT_USERNAME = "bcsotty"
CLIENT_PASSWORD = "correct"
FIRE_ALARM_ER_PREFIX = config.get("TOPICS", "emergency_alarm") 
FIRE_ALARM_RESPONSE_PREFIX = config.get("TOPICS", "controller_response")
MQTTMessage = "ALERT."

# Topics
FIRE_ALARM_ER_TOPIC = FIRE_ALARM_ER_PREFIX + "/" + CLIENT_USERNAME
FIRE_ALARM_RESPONSE_TOPIC = FIRE_ALARM_RESPONSE_PREFIX + "/" + CLIENT_USERNAME

# BROKER_HOST = "mqtt.eclipseprojects.io"
    
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    if(rc == 5):
        print("Authentication Error on Broker")
        exit()
    print("Connected to Broker with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    print(f"Sending: {MQTTMessage} to topic {FIRE_ALARM_ER_TOPIC}")
    publish.single(FIRE_ALARM_ER_TOPIC, MQTTMessage, hostname = BROKER_HOST, auth={'username':CLIENT_USERNAME, 'password':CLIENT_PASSWORD})
    client.subscribe(FIRE_ALARM_RESPONSE_TOPIC)
    print(f"Subscribed to: {FIRE_ALARM_RESPONSE_TOPIC}")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload.decode()))
    time.sleep(5)
    publish.single(FIRE_ALARM_ER_TOPIC, MQTTMessage, hostname = BROKER_HOST, port = 1883, auth={'username':CLIENT_USERNAME, 'password':CLIENT_PASSWORD})
    # When a message is received, a response is published
    # publish_response(FIRE_ALARM_ER_TOPIC, "Hello again, from Simple-Client-Publish", "mqtt.eclipseprojects.io")

def main():

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    # Set Username and Password
    client.username_pw_set(username=CLIENT_USERNAME, password=CLIENT_PASSWORD )
    # Connect to broker
    client.connect(BROKER_HOST, 1883)

    while True: 
        client.loop()


if __name__ == "__main__":
    main()