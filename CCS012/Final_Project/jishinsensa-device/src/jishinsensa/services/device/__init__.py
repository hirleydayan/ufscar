"""Device module."""
import multiprocessing
from jishinsensa.services.device.sensors import Sensor

sensors = []


def add_sensor(sensor):
    """Add sensor to sensors list."""
    if isinstance(sensor, Sensor):
        sensors.append(sensor)
        return True
    else:
        return False


def run_sensors():
    """Read sensor loop."""
    for s in sensors:
        p = multiprocessing.Process(target=s.run)
        p.start()
