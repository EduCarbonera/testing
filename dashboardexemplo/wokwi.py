import network
import time
from machine import Pin
import dht
import ujson
from umqtt.simple import MQTTClient

# MQTT Server Parameters
MQTT_CLIENT_ID = "micropython-weather-demo"
MQTT_BROKER    = "broker.mqttdashboard.com"
MQTT_USER      = ""
MQTT_PASSWORD  = ""
MQTT_TOPIC1    = "/aula/temperature1"
MQTT_TOPIC2    = "/aula/humidity"
MQTT_TOPIC_ACTUATOR = "/actuator"

sensor = dht.DHT22(Pin(15))
led_mqtt = Pin(16, Pin.OUT)

print("Connecting to WiFi", end="")
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('Wokwi-GUEST', '')
while not sta_if.isconnected():
    print(".", end="")
    time.sleep(0.1)
print(" Connected!")

print("Connecting to MQTT server... ", end="")
client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, user=MQTT_USER, password=MQTT_PASSWORD)
client.connect()

# Define callback para receber mensagens MQTT
def mqtt_callback(topic, msg):
    print("Received message:", topic, msg)
    if topic == b"/actuator":
        if msg == b"1":
            led_mqtt.value(1)  # liga LED
        else:
            led_mqtt.value(0)  # desliga LED

client.set_callback(mqtt_callback)
client.subscribe(MQTT_TOPIC_ACTUATOR.encode())

print("Connected!")

prev_weather = ""
while True:
    client.check_msg()

    print("Measuring weather conditions... ", end="")
    sensor.measure() 
    message = ujson.dumps({
        "temp": sensor.temperature(),
        "humidity": sensor.humidity(),
    })
    if message != prev_weather:
        print("Updated!")
        client.publish(MQTT_TOPIC1, str(sensor.temperature()))
        client.publish(MQTT_TOPIC2, str(sensor.humidity()))
        prev_weather = message
    else:
        print("No change")
    time.sleep(1)
