from libsoc_zero.GPIO import LED
from libsoc_zero.GPIO import Button

from time import sleep

led = LED('GPIO-C')
btn = Button('GPIO-A')

while True:
    sleep(0.25)
    if btn.is_pressed():
        led.on()
        print('Button is pressed!')
    else:
        led.off()
        print('Button is not pressed!')

