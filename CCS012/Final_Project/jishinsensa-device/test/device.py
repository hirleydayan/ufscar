#!/usr/bin/env python3
"""Device small test program."""
import jishinsensa.services.device as device

from jishinsensa.services.device.sensors import Tilt
from jishinsensa.services.device.sensors import Temperature
from jishinsensa.services.device.sensors import LDR

if __name__ == '__main__':
    device.add_sensor(Temperature())
    device.add_sensor(Tilt())
    device.add_sensor(LDR())
    device.run_sensors()
