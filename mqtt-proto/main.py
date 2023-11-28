import asyncio
import asyncio_mqtt
import aiohttp

FIRE_ALARM_ER_TOPIC = "/FireAlarm"

async def on_connect(client, flags, rc):
    print("Connected to Fire Alarm. Result Code:", rc)
    await client.subscribe(FIRE_ALARM_ER_TOPIC)

async def on_message(client, topic, payload, qos, properties):
    print(payload.decode())
    # Call API asynchronously
    async with aiohttp.ClientSession() as session:
        async with session.post("http://localhost:8080/notify", data={"message": payload.decode()}) as response:
            if response:
                print(response.status)
            else:
                print("An error occurred with the response")

async def main():
    client = asyncio_mqtt.Client("mqtt.eclipseprojects.io")
    client.on_connect = on_connect
    client.on_message = on_message

    await client.connect()

    # Continuously receive messages in an event loop
    async with client.filtered_messages(FIRE_ALARM_ER_TOPIC) as messages:
        async for message in messages:
            await on_message(client, message.topic, message.payload, message.qos, message.properties)

asyncio.run(main())
