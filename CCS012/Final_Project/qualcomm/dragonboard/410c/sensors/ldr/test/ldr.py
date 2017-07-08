"""Temperature test module."""
import qcom_db_410c.sensors.ldr as ldr
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
        channel = [0x01, 0x80, 0x00]
        gpio_cs = gpio.GPIO(18, gpio.DIRECTION_OUTPUT)
        tp = ldr.LDR(gpio_cs, spi, channel)
    else:
        tp = ldr.LDR()

    print("ADC: %.2f" % tp.get_adc())
    print("Volts: %.2f" % tp.get_volts())
    print("Lux: %.2f" % tp.get_lux())
