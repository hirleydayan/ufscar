#!/usr/bin/env python3
"""Temperature test module."""
import qcom_db_410c.sensors.ldr as ldr
import platform
import re

TARGET_ID = "qcom"

if __name__ == '__main__':
    if re.search(TARGET_ID, platform.platform()):
        import spidev
        from libsoc import gpio
        spi = spidev.SpiDev()
        spi.open(0, 0)
        spi.max_speed_hz = 10000
        spi.mode = 0b00
        spi.bits_per_word = 8
        channel = [0x01, 0x80, 0x00]
        gpio_cs = gpio.GPIO(18, gpio.DIRECTION_OUTPUT)
        tp = ldr.LDR("test_ldr_sensor", gpio_cs, spi, channel)
    else:
        tp = ldr.LDR("test_ldr_sensor")

    print("ADC [%s]: %.2f" % (tp.get_id(), tp.get_adc()))
    print("Volts [%s]: %.2f" % (tp.get_id(), tp.get_volts()))
    print("Lux [%s]: %.2f" % (tp.get_id(), tp.get_lux()))
