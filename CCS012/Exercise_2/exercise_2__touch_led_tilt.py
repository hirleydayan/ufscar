"""Class 2 - DragonBoard start kit and MQTT."""
from libsoc_zero.GPIO import LED
from libsoc_zero.GPIO import Button
from libsoc_zero.GPIO import Tilt
from time import sleep

import datetime
import sys

led = LED('GPIO-E')
touch = Button('GPIO-A')
tilt = Tilt('GPIO-C')

if __name__ == '__main__':
    try:
        file22 = open('./act2exerc2.txt', 'w')
        file22.write('##############################################\n')
        file22.write('    Exercise 2 for Activity2, UFSCar 2017     \n')
        file22.write(' Edvaldo Santos, Hirley Silva, Helio Nakazato \n')
        file22.write('##############################################\n')

        while True:
            sleep(0.25)
            timestamp = '{:%Y-%b-%d %H:%M:%S}'.format(datetime.datetime.now())
            if touch.is_pressed():
                led.on()
                file22.write(timestamp + ' --  Touch sensor is pressed!\n')
            else:
                led.off()
                file22.write(timestamp + ' --  Touch sensor is not pressed!\n')

            if tilt.is_tilted():
                file22.write(timestamp + ' --  Tilt sensor is changed!\n')
            else:
                file22.write(timestamp + ' --  Tilt sensor is normal!\n')

    except KeyboardInterrupt:
        file22.close()
        sys.exit(0)
