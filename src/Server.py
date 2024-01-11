import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish #publish dependency
import requests # to send API request to PWA

# Constants
FIRE_ALARM_ER_TOPIC = "/FireAlarm"
PWA_PUSH_URL = "http://localhost:3000/notify"
BROKER_HOST = "mqtt.eclipseprojects.io"

# The callback for when the client receives a CONNACK response from the broker.
def on_connect(client, userdata, flags, rc):
    print("Connected to Fire Alarm. Result Code: "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # subscribing to FireAlarm topic
    client.subscribe(FIRE_ALARM_ER_TOPIC)

# The callback for when a message is published to the broker, and the backendreceives it
def on_message(client, userdata, msg):
    # Print MQTT message to console
    print(msg.payload.decode())
    # Create Body for POST to PWA
        # sub: Push Notification Subscription
        # notification: Contains fields that appear on native push notification
    data = {
    "username": "bcsotty",
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

# Executed when script is ran

# create MQTT Client
client = mqtt.Client()
# Set Paho API functions to our defined functions
client.on_connect = on_connect
client.on_message = on_message
# Connect client to the Broker
client.connect(BROKER_HOST, 1883, 60)
# Run cliet forever
while True:
    client.loop()
