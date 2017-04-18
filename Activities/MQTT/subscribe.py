#!/usr/bin/env python3
"""MQTT Activity."""
# https://blog.butecopensource.org/mqtt-parte-2-enviando-e-recebendo-mensagens/
import paho.mqtt.client as mqtt
import sys

MQTT_ADDRESS = 'iot.eclipse.org'
# MQTT_ADDRESS = 'broker.hivemq.com'
MQTT_PORT = 1883
MQTT_TIMEOUT = 600
# MQTT_TOPIC = '/ccs012/hirley_helio'

if sys.version_info[0] == 3:
    input_func = input
else:
    input_func = raw_input


def on_connect(client, userdata, flags, rc):
    """On connect."""
    print('Connected. Result: %s' % str(rc))
    result, message_id = client.subscribe(topic, qos=0)
    print('Subscribing on topic "%s" (%d)' % (topic, message_id))


def on_message(client, userdata, msg):
    """On message."""
    if msg.topic == topic:
        print('Received message "%s" on topic "%s"' % (msg.payload, msg.topic))
        print('Message: %s' % msg.payload)
    else:
        print('Unknown topic.')


def loop():
    """Loop."""
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    # client.username_pw_set(MQTT_AUTH.user, MQTT_AUTH.pwd)
    client.connect(MQTT_ADDRESS, MQTT_PORT, MQTT_TIMEOUT)
    client.loop_forever()


if __name__ == '__main__':
    global topic
    topic = input_func('Enter MQTT subscribing topic: ')
    loop()
