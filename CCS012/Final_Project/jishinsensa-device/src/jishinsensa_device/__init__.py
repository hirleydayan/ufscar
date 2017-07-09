"""Device routines."""
__import__('pkg_resources').declare_namespace(__name__)
import qcom_db_410c.sensors.temperature as dbtmp
import platform
import re

import threading

TARGET_ID = "qcom"
TEMPERATURE_ID = "temperature"


class Temperature:
    """Temperature sensor device routine."""

    def __init__(self):
        """Init temperature sensor."""
        if re.search(TARGET_ID, platform.platform()):
            import spidev
            from libsoc import gpio
            spi = spidev.SpiDev()
            spi.open(0, 0)
            spi.max_speed_hz = 10000
            spi.mode = 0b00
            spi.bits_per_word = 8
            channel = [0x01, 0xA0, 0x00]
            gpio_cs = gpio.GPIO(18, gpio.DIRECTION_OUTPUT)
            self.temp_sensor = dbtmp.Temperature(TEMPERATURE_ID,
                                                 gpio_cs, spi, channel)
        else:
            self.temp_sensor = dbtmp.Temperature(TEMPERATURE_ID)

    def sense_loop(self):
        """Read sensor loop."""
        t1 = threading.Thread(target=self.temp_sensor.get_celsius())
        t1.start()
