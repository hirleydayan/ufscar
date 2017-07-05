from libsoc_zero.GPIO import LED
from libsoc_zero.GPIO import Button

from time import sleep

import datetime

led = LED('GPIO-C')
touch = Button('GPIO-A')

file22 = open('./act2exerc2.txt', 'w')

print('#############################################', file = file22)
print('    Exercise 2 for Activity2, UFSCar 2017    ', file = file22)
print('Edvaldo Santos, Hirley Silva, Helio Nakazato ', file = file22)
print('#############################################', file = file22)

while True:
    sleep(0.5)
    timestamp = '{:%Y-%b-%d %H:%M:%S}'.format(datetime.datetime.now())
    if touch.is_pressed():
        led.on()
        print(timestamp, ' --  Touch sensor is pressed!', file = file22)
    else:
        led.off()
        print(timestamp, ' --  Touch sensor is not pressed!', file = file22)

