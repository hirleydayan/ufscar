"""Device sensors module."""
import qcom_db_410c.ldr as dbldr
import qcom_db_410c.gps as dbgps
import qcom_db_410c.temperature as dbtmp
import qcom_db_410c.tilt as dbtlt
import platform
import re

from abc import ABC, abstractmethod

# Identifications
ID_HW_TARGET = "qcom"

ID_GPS = "gps"
ID_LUX = "lux"
ID_TEM = "temperature"
ID_TIL = "tilt"

DECIMAL_PRECISION = 2


class Sensor(ABC):
    """Sensor device routine."""

    @abstractmethod
    def get(self):
        """Get sensor data."""
        raise NotImplementedError


class Temperature(Sensor):
    """Temperature sensor."""

    def __init__(self):
        """Init temperature sensor."""
        if re.search(ID_HW_TARGET, platform.platform()):
            import spidev
            from libsoc import gpio
            spi = spidev.SpiDev()
            spi.open(0, 0)
            spi.max_speed_hz = 10000
            spi.mode = 0b00
            spi.bits_per_word = 8
            channel = [0x01, 0xA0, 0x00]
            gpio_cs = gpio.GPIO(18, gpio.DIRECTION_OUTPUT)
            self.temp_sensor = dbtmp.Temperature(ID_TEM, gpio_cs, spi, channel)
        else:
            self.temp_sensor = dbtmp.Temperature(ID_TEM)

    def get(self):
        """Get sensor data."""
        return (self.temp_sensor.get_id(),
                round(self.temp_sensor.get_celsius(), DECIMAL_PRECISION))


class Tilt(Sensor):
    """Tilt sensor."""

    def __init__(self):
        """Init tilt sensor."""
        if re.search(ID_HW_TARGET, platform.platform()):
            self.tilt_sensor = dbtlt.Tilt(ID_TIL, 'GPIO-C')
        else:
            self.tilt_sensor = dbtlt.Tilt(ID_TIL)

    def get(self):
        """Get sensor data."""
        return (self.tilt_sensor.get_id(), self.tilt_sensor.get_state())


class GPS(Sensor):
    """GPS sensor."""

    def __init__(self, simulated_coordinates=None):
        """Init GPS sensor."""
        self.gps_sensor = None
        if re.search(ID_HW_TARGET, platform.platform()):
            self.gps_sensor = dbgps.GPS(ID_GPS)
        else:
            if simulated_coordinates is not None:
                self.gps_sensor = dbgps.GPS(ID_GPS, simulated_coordinates)

    def get(self):
        """Get sensor data."""
        return (self.gps_sensor.get_id(), self.gps_sensor.get_coordinates())


class Lux(Sensor):
    """LDR sensor."""

    def __init__(self):
        """Init LDR sensor."""
        if re.search(ID_HW_TARGET, platform.platform()):
            import spidev
            from libsoc import gpio
            spi = spidev.SpiDev()
            spi.open(0, 0)
            spi.max_speed_hz = 10000
            spi.mode = 0b00
            spi.bits_per_word = 8
            channel = [0x01, 0x80, 0x00]
            gpio_cs = gpio.GPIO(18, gpio.DIRECTION_OUTPUT)
            self.ldr_sensor = dbldr.LDR(ID_LUX, gpio_cs, spi, channel)
        else:
            self.ldr_sensor = dbldr.LDR(ID_LUX)

    def get(self):
        """Get sensor data."""
        return (self.ldr_sensor.get_id(),
                round(self.ldr_sensor.get_lux(), DECIMAL_PRECISION))
