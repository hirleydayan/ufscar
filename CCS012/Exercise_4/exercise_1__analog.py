"""Class 4 - OpenHAB Integration."""
import spidev

from libsoc_zero.GPIO import LED
from libsoc_zero.GPIO import Button
from libsoc import gpio
from time import sleep

import paho.mqtt.client as mqtt
import sys

led_counter = 0

# Servidor eclipse que roda o mosquitto(um broker)
MQTT_ADDRESS = 'localhost'
# MQTT_ADDRESS = 'broker.hivemq.com'
MQTT_PORT = 1883
MQTT_TIMEOUT = 60
MQTT_DEFAULT_QOS = 0
MQTT_TOPIC = 'analog'
# MQTT_TOPIC = '/hirleydayan/dev'

LAST_WILL_DEFAULT_MSG = 0
LAST_WILL_DEFAULT_QOS = 1
LAST_WILL_DEFAULT_RETAIN = True

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 10000
spi.mode = 0b00
spi.bits_per_word = 8
channel_select = [0x01, 0xA0, 0x00]

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
        gpio_cs = gpio.GPIO(18, gpio.DIRECTION_OUTPUT)
        with gpio.request_gpios([gpio_cs]):
            while True:
                sleep(5)
                gpio_cs.set_high()
                sleep(0.00001)
                gpio_cs.set_low()
                rx = spi.xfer(channel_select)
                gpio_cs.set_high()
                adc_value = (rx[1] << 8) & 0b1100000000
                adc_value = adc_value | (rx[2] & 0xff)
                print(adc_value)
                send_message(topic, client, adc_value, 1)

    except KeyboardInterrupt:
        sys.exit(0)
