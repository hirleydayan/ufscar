"""Temperature test module."""
import qcom_db_410c.sensors.temperature as t
import spidev
import platform
import re

from libsoc import gpio

TARGET_ID = "qcom"

if __name__ == '__main__':
    if re.search(TARGET_ID, platform.platform()):
        spi = spidev.SpiDev()
        spi.open(0, 0)
        spi.max_speed_hz = 10000
        spi.mode = 0b00
        spi.bits_per_word = 8
        channel = [0x01, 0xA0, 0x00]
        gpio_cs = gpio.GPIO(18, gpio.DIRECTION_OUTPUT)
        tp = t.Temperature(gpio_cs, spi, channel)
    else:
        tp = t.Temperature()

    print("ADC: %.2f" % tp.get_adc())
    print("Volts: %.2f" % tp.get_volts())
    print("Celcius: %.2f" % tp.get_celsius())
    print("Fahrenheight: %.2f" % tp.get_fahrenheight())
