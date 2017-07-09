"""Temperature test module."""
import qcom_db_410c.sensors.temperature as t
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
        channel = [0x01, 0xA0, 0x00]
        gpio_cs = gpio.GPIO(18, gpio.DIRECTION_OUTPUT)
        tp = t.Temperature("test_temperature_sensor", gpio_cs, spi, channel)
    else:
        tp = t.Temperature("test_temperature_sensor")

    print("ADC [%s]: %.2f" % (tp.get_id(), tp.get_adc()))
    print("Volts [%s]: %.2f" % (tp.get_id(), tp.get_volts()))
    print("Celcius [%s]: %.2f" % (tp.get_id(), tp.get_celsius()))
    print("Fahrenheight [%s]: %.2f" % (tp.get_id(), tp.get_fahrenheight()))
