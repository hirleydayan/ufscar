from libsoc_zero.GPIO import LED
from libsoc_zero.GPIO import Button

from time import sleep

led = LED('GPIO-C')
btn = Button('GPIO-B')

while True:
    btn.wait_for_press()

    if led.is_lit():
        led.off()
    else:
        led.on()

    sleep(1)
