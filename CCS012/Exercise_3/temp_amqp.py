"""Activity 3."""
import spidev
from libsoc import gpio
from time import sleep

import pika
import sys

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 10000
spi.mode = 0b00
spi.bits_per_word = 8
channel_select = [0x01, 0xA0, 0x00]

if __name__ == '__main__':

    try:
        print("AMQP temp producer started...")
        pika.PlainCredentials('linaro', 'linaro')
        connection = pika.BlockingConnection(
                        pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='hello_temp')

        gpio_cs = gpio.GPIO(18, gpio.DIRECTION_OUTPUT)
        with gpio.request_gpios([gpio_cs]):
            while True:
                gpio_cs.set_high()
                sleep(0.00001)
                gpio_cs.set_low()
                rx = spi.xfer(channel_select)
                gpio_cs.set_high()

                adc_value = (rx[1] << 8) & 0b1100000000
                adc_value = adc_value | (rx[2] & 0xff)

                print(" [x] Producing 'ADC Value: %d'" % adc_value)
                channel.basic_publish(exchange='',
                                      routing_key='hello_temp',
                                      body="ADC Value: %d" % adc_value)


                sleep(1)
    except KeyboardInterrupt:
        connection.close()
        print("Finished.")
        sys.exit(0)
