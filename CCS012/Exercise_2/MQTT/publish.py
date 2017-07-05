#!/usr/bin/env python3
"""MQTT Activity."""
# https://blog.butecopensource.org/mqtt-parte-2-enviando-e-recebendo-mensagens/
import paho.mqtt.client as mqtt
import sys
# import time
# from os import walk

# Servidor eclipse que roda o mosquitto(um broker)
MQTT_ADDRESS = 'iot.eclipse.org'
# MQTT_ADDRESS = 'broker.hivemq.com'
MQTT_PORT = 1883
MQTT_TIMEOUT = 60
MQTT_DEFAULT_QOS = 0
# MQTT_TOPIC = '/ccs012/hirley_helio'
# MQTT_TOPIC = '/hirleydayan/dev'

LAST_WILL_DEFAULT_MSG = "Publisher disconnected"
LAST_WILL_DEFAULT_QOS = 0
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
    print('Sent message - id: %d, QoS: %d' % (message_id, qos))


if __name__ == '__main__':
    topic = input_func('Enter MQTT publishing topic: ')
    l_msg = input_func('Enter last will message: ')
    l_qos = input_func('Enter last will QoS: ')
    client = on_connect(topic, l_msg, int(l_qos))
    previous_qos = MQTT_DEFAULT_QOS
    qos = previous_qos
    while True:
        msg = input_func('Enter message: ')
        qos = input_func('Enter QoS (%d): ' % previous_qos)
        if qos == '':
            qos = previous_qos
        else:
            previous_qos = int(qos)
        send_message(topic, client, msg, int(qos))
