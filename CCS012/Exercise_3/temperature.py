"""Activity 3."""
import spidev
from libsoc import gpio
from time import sleep
import time
import sys
import datetime

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 10000
spi.mode = 0b00
spi.bits_per_word = 8
channel_select = [0x01, 0xA0, 0x00]

if __name__ == '__main__':
    try:
        print("Started...")
        f = open('./act3exerc1.txt', 'w')
        f.write('##############################################\n')
        f.write('    Exercise 1 for Activity3, UFSCar 2017     \n')
        f.write(' Edvaldo Santos, Hirley Silva, Helio Nakazato \n')
        f.write('##############################################\n')

        timeout = 120
        timeout_start = time.time()

        gpio_cs = gpio.GPIO(18, gpio.DIRECTION_OUTPUT)
        with gpio.request_gpios([gpio_cs]):
            while time.time() <= timeout_start + timeout:
                sleep(5)
                gpio_cs.set_high()
                sleep(0.00001)
                gpio_cs.set_low()
                rx = spi.xfer(channel_select)
                gpio_cs.set_high()
                adc_value = (rx[1] << 8) & 0b1100000000
                adc_value = adc_value | (rx[2] & 0xff)
                timestamp = '{:%Y-%b-%d %H:%M:%S}'.\
                            format(datetime.datetime.now())
                print("[%s] ADC Value: %d" % (timestamp, adc_value))
                f.write("[%s] ADC Value: %d\n" % (timestamp, adc_value))
    except KeyboardInterrupt:
        f.close()
        sys.exit(0)
