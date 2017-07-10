"""Device sensors module."""
import qcom_db_410c.sensors.temperature as dbtmp
import qcom_db_410c.sensors.tilt as dbtlt
import qcom_db_410c.sensors.ldr as dbldr
import platform
import re

from abc import ABC, abstractmethod
from time import sleep

# Identifications
TARGET_ID = "qcom"
TEM_ID = "temperature"
TIL_ID = "tilt"
LDR_ID = "ldr"

# Delays
TEM_READING_DELAY = 5
TIL_READING_DELAY = 5
LDR_READING_DELAY = 5


class Sensor(ABC):
    """Sensor device routine."""

    @abstractmethod
    def run(self):
        """Get sensor data."""
        raise NotImplementedError


class Temperature(Sensor):
    """Temperature sensor."""

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
            self.temp_sensor = dbtmp.Temperature(TEM_ID, gpio_cs, spi, channel)
        else:
            self.temp_sensor = dbtmp.Temperature(TEM_ID)

    def run(self):
        """Get temperature in celsius."""
        while True:
            print(self.temp_sensor.get_celsius())
            sleep(TEM_READING_DELAY)


class Tilt(Sensor):
    """Tilt sensor."""

    def __init__(self):
        """Init tilt sensor."""
        if re.search(TARGET_ID, platform.platform()):
            self.tilt_sensor = dbtlt.Tilt(TIL_ID, 'GPIO-C')
        else:
            self.tilt_sensor = dbtlt.Tilt(TIL_ID)

    def run(self):
        """Get tilt in celsius."""
        while True:
            print(self.tilt_sensor.get_state())
            sleep(TIL_READING_DELAY)


class LDR(Sensor):
    """LDR sensor."""

    def __init__(self):
        """Init LDR sensor."""
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
            self.ldr_sensor = dbldr.LDR(LDR_ID, gpio_cs, spi, channel)
        else:
            self.ldr_sensor = dbldr.LDR(LDR_ID)

    def run(self):
        """Get LDR lux."""
        while True:
            print(self.ldr_sensor.get_lux())
            sleep(LDR_READING_DELAY)
