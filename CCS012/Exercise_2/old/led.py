from libsoc_zero.GPIO import LED
from time import sleep

led = LED('GPIO-C')

while True:
    led.on()
    sleep(1)
    led.off()
    sleep(1)
