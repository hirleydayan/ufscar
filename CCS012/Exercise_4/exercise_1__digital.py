"""Class 4 - OpenHAB Integration."""
from libsoc_zero.GPIO import LED
from libsoc_zero.GPIO import Button
from libsoc import gpio

import paho.mqtt.client as mqtt
import sys

led = LED('GPIO-E')
touch = Button('GPIO-A')

# Servidor eclipse que roda o mosquitto(um broker)
MQTT_ADDRESS = 'localhost'
# MQTT_ADDRESS = 'broker.hivemq.com'
MQTT_PORT = 1883
MQTT_TIMEOUT = 60
MQTT_DEFAULT_QOS = 0
MQTT_TOPIC = 'digital'
# MQTT_TOPIC = '/hirleydayan/dev'

LAST_WILL_DEFAULT_MSG = 0
LAST_WILL_DEFAULT_QOS = 1
LAST_WILL_DEFAULT_RETAIN = True

if sys.version_info[0] == 3:
    input_func = input
else:
    input_func = raw_input


def on_connect(topic, last_will_msg=LAST_WILL_DEFAULT_MSG,
               last_will_qos=LAST_WILL_DEFAULT_QOS):
    """On connect."""
    client = mqtt.Client(protocol=mqtt.MQTTv311)
    client.will_set(topic, last_will_msg, last_will_qos,
                    retain=LAST_WILL_DEFAULT_RETAIN)
    client.connect(MQTT_ADDRESS, MQTT_PORT, MQTT_TIMEOUT)
    client.loop_start()
    return client


def send_message(topic, client, msg, qos=MQTT_DEFAULT_QOS):
    """Send message."""
    result, message_id = client.publish(topic, msg, qos=qos)


if __name__ == '__main__':
    try:
        print('MQTT publishing topic: ' + MQTT_TOPIC)
        topic = MQTT_TOPIC
        client = on_connect(topic)
        send_message(topic, client, "Connected", 1)

        while True:
            touch.wait_for_press()
            if led.is_lit:
                led.off()
                send_message(topic, client, "0", 1)
            else:
                led.on()
                send_message(topic, client, "1", 1)

    except KeyboardInterrupt:
        sys.exit(0)
