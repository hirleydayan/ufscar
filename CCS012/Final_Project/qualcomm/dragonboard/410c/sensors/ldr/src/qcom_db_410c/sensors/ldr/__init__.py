"""Temperature sensor module."""
import platform
import re

from random import uniform
from time import sleep

TARGET_ID = "qcom"


class LDR:
    """LDR sensor."""

    def __init__(self, id, gpio=None, spi=None, channel=None):
        """Init ldr sensor."""

        if id is None:
            raise ValueError("id must not be None")

        self.id = id

        if spi is None or \
           channel is None or \
           gpio is None:
            if re.search(TARGET_ID, platform.platform()):
                if gpio is None:
                    raise ValueError("gpio must not be None")
                if spi is None:
                    raise ValueError("spi must not be None")
                if channel is None:
                    raise ValueError("channel must not be None")
            return
        if re.search(TARGET_ID, platform.platform()):
            self.spi = spi
            self.channel = channel
            self.gpio_cs = gpio

    def get_adc(self):
        """Read analog pin."""
        if re.search(TARGET_ID, platform.platform()):
            from libsoc import gpio
            with gpio.request_gpios([self.gpio_cs]):
                self.gpio_cs.set_high()
                sleep(0.00001)
                self.gpio_cs.set_low()
                rx = self.spi.xfer(self.channel)
                self.gpio_cs.set_high()
                adc_value = (rx[1] << 8) & 0b1100000000
                adc_value = adc_value | (rx[2] & 0xff)
                # adc_value = (rx[1] & 3) << 8 | rx[2]
        else:
            adc_value = uniform(130.0, 150.0)
        return adc_value

    def get_id(self):
        """Get sensor ID."""
        return self.id

    def get_volts(self):
        """Get volts."""
        return (self.get_adc() * 3.3) / 1023

    def get_lux(self, r=10):
        """Get lux."""
        return 500 * (3.3 - self.get_volts())/(r * self.get_volts())
