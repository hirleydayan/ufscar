"""Activity 3."""
import spidev
from libsoc import gpio

import pika
import sys

from libsoc_zero.GPIO import LED
from libsoc_zero.GPIO import Button
from libsoc_zero.GPIO import Tilt

import datetime

led = LED('GPIO-E')
touch = Button('GPIO-A')
tilt = Tilt('GPIO-C')

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 10000
spi.mode = 0b00
spi.bits_per_word = 8
channel_select = [0x01, 0xA0, 0x00]

if __name__ == '__main__':

    try:
        print("AMQP touch producer started...")
        pika.PlainCredentials('linaro', 'linaro')
        connection = pika.BlockingConnection(
                        pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='hello_touch')

        gpio_cs = gpio.GPIO(18, gpio.DIRECTION_OUTPUT)
        while True:
            timestamp = '{:%Y-%b-%d %H:%M:%S}'.format(datetime.datetime.now())
            touch.wait_for_press()
            print(" [x] Producing 'Touch on at %s'" % timestamp)
            channel.basic_publish(exchange='',
                                  routing_key='hello_touch',
                                  body="Touch on at %s'" % timestamp)
    except KeyboardInterrupt:
        connection.close()
        print("Finished.")
        sys.exit(0)
