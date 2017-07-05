"""Temperature sensor module."""
# Connected to ADC2
import platform
import re

from random import uniform

TARGET_ID = "qcom"


class Temperature:
    """Temperature sensor."""

    # spi = spidev.SpiDev()
    # spi.open(0, 0)
    # spi.max_speed_hz = 10000
    # spi.mode = 0b00
    # spi.bits_per_word = 8
    # channel_select = [0x01, 0xA0, 0x00]
    # gpio.DIRECTION_OUTPUT
    # gpio = 18
    # gpio_cs = gpio.GPIO(18, gpio.DIRECTION_OUTPUT)
    #
    # import spidev
    # from libsoc import gpio

    def __init__(self, gpio=None, spi=None, channel=None):
        """Init temperature sensor."""
        if spi is None and \
           channel is None and \
           gpio is None:
            return
        if re.search(TARGET_ID, platform.platform()):
            self.spi = spi
            self.channel = channel
            self.gpio_cs = gpio

    def __get_adc(self):
        if re.search(TARGET_ID, platform.platform()):
            from libsoc import gpio
            self.gpio_cs.set_high()
            with gpio.request_gpios([self.gpio_cs]):
                self.gpio_cs.set_low()
                rx = self.spi.xfer(self.channel)
                self.gpio_cs.set_high()
                adc_value = (rx[1] << 8) & 0b1100000000
                adc_value = adc_value | (rx[2] & 0xff)
        else:
            adc_value = uniform(20.0, 25.0)
        return adc_value

    def get_celsius(self):
        """Get temperature."""
        return self.__get_adc()


if __name__ == '__main__':
    if re.search(TARGET_ID, platform.platform()):
        import spidev
        from libsoc import gpio
        spi = spidev.SpiDev()
        spi.open(0, 0)
        spi.max_speed_hz = 10000
        spi.mode = 0b00
        spi.bits_per_word = 8
        channel = [0x01, 0xA0, 0x00]
        gpio = gpio.GPIO(18, gpio.DIRECTION_OUTPUT)
        temperature_c = Temperature(gpio, spi, channel)
    else:
        temperature_c = Temperature()
    print("Temperature C: %d" % temperature_c.get_celsius())
