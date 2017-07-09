"""Device sensors module."""
import qcom_db_410c.sensors.temperature as dbtmp
import platform
import re

from threading import Thread
from time import sleep

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
        t1 = Thread(target=self.get_temperature_celsius)
        t1.start()

    def get_temperature_celsius(self):
        while True:
            print(self.temp_sensor.get_celsius())
            sleep(5)

if __name__ == '__main__':
    Temperature().sense_loop()
