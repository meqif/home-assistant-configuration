#!/usr/bin/env python

import sys
import inkyphat
import paho.mqtt.client as mqtt

from time import sleep
from PIL import ImageFont

TEMPERATURE_SENSOR = "livingroom/sensor/bme280_temperature/state"
HUMIDITY_SENSOR = "livingroom/sensor/bme280_relative_humidity/state"

if len(sys.argv) < 2:
    print("""Usage: {} <mqtt server>""".format(sys.argv[0]))
    sys.exit(1)

mqtt_server_hostname = sys.argv[1]

#inkyphat.set_rotation(180)
inkyphat.set_colour("black")

temperature = "--.-"
previous_temperature = None
humidity = "--.-"
previous_humidity = None

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(TEMPERATURE_SENSOR)
    client.subscribe(HUMIDITY_SENSOR)

def on_message(client, userdata, msg):
    global temperature, humidity

    if msg.topic == TEMPERATURE_SENSOR:
        temperature = msg.payload.decode("utf-8")
        print("Received temperature " + temperature)
    elif msg.topic == HUMIDITY_SENSOR:
        humidity = msg.payload.decode("utf-8")
        print("Received humidity " + humidity)
    else:
        print(msg.topic + " " + str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(mqtt_server_hostname, 1883, 60)
client.loop_start()

sleep(5)
while True:
    if previous_temperature != temperature or previous_humidity != humidity:
        previous_temperature = temperature
        previous_humidity = humidity

        inkyphat.clear()

        # Humidity update
        font = ImageFont.truetype('assets/digital-7.ttf', 40)
        humidity_text = humidity + "%"
        w, h = font.getsize(humidity_text)
        inkyphat.text((5, 5), humidity_text, inkyphat.BLACK, font)

        # Temperature update
        font = ImageFont.truetype('assets/digital-7.ttf', 80)
        temperature_text = temperature + '`C'
        w, h = font.getsize(temperature_text)
        x = 0
        y = (inkyphat.HEIGHT) - h - 5
        inkyphat.text((x, y), temperature_text, inkyphat.BLACK, font)

        inkyphat.show()

    sleep(60)
