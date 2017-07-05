#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
needs spidev installed
http://www.raspberrypi-spy.co.uk/2014/08/enabling-the-spi-interface-on-the-raspberry-pi/
'''
import sys

import time
import spidev

pd = 0 # S connected to A0

spi = spidev.SpiDev()
spi.open(0,0)

def readadc(adcnum):
        # read SPI data from MCP3004 chip, 4 possible adc’s (0 thru 3)
        if ((adcnum > 3) or (adcnum < 0)):
            return-1
        r = spi.xfer2([1,8+adcnum <<4,0])
        #print(r)
        adcout = ((r[1] &3) <<8)+r[2]
        #print(adcout)
        return adcout


tolerance = 0.5   # degrees
value = readadc(pd)
# calibrate the formula with a termometer
lasttemp = 125.315 - 0.175529 * value   # temperature formula made through Wolfram Alpha: 'linear function (0,125);(720,0);(1023,-55)', where (readvalue, temperature)
print('Temperature: %5.2fC (input: %3d)' % (lasttemp, value))
while True:
        value = readadc(pd)
        temp = 125.315 - 0.175529 * value  # temperature formula
        if ((temp > lasttemp + tolerance) or (temp < lasttemp - tolerance)):  # if temperature changed more than the tolerance
                print('New temperature: %5.2fC (input: %3d)' % (temp, value))
                lasttemp = temp
        time.sleep(0.1)

print('done.')


#!/usr/bin/env python3

from time import sleep
from libsoc import gpio
from libsoc import spi

# This test is intended to be run with sliding rheostat module
# connecting to ADC1 port on Linker Base Mezzanine Card on dragonboard410c.


def main():
    spi.SPI.set_debug(1)
    gpio_cs = gpio.GPIO(18, gpio.DIRECTION_OUTPUT)
    with gpio.request_gpios([gpio_cs]):
        tx = b'\x01\x80\x00'
        with spi.SPI(0, 0, spi.MODE_0, 10000, spi.BITS_8) as spi_dev:
            while True:
                gpio_cs.set_high()
                sleep(0.00001)
                gpio_cs.set_low()
                rx = spi_dev.rw(3, tx)
                gpio_cs.set_high()

                adc_value = (rx[1] << 8) & 0b1100000000
                adc_value = adc_value | (rx[2] & 0xff)

                print("adc_value: %d" % adc_value)
                sleep(1)

if __name__ == '__main__':
    main()
