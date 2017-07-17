"""Device module."""
import json
import multiprocessing as mp

from jishinsensa.services.device.sensors import Sensor
from time import sleep
from time import time

DELAY_RUN = 5000
DELAY_AGGREGATOR = 10000

KEY_PUB_TOPIC = "pub_topic"
KEY_DEVICE_ID = "device_id"

DEFAULT_PUB_TOPIC = "event"
DEFAULT_SUB_TOPIC = "command"
DEFAULT_DEVICE_ID = "device"

__sensors = []
__agg_dictionary = []


def add_sensor(sensor):
    """Add sensor to sensors list."""
    if isinstance(sensor, Sensor):
        __sensors.append(sensor)
        return True
    else:
        return False


def run(sensor_delay=DELAY_RUN, aggregator_delay=DELAY_AGGREGATOR,
        publishers=None):
    """Read sensors."""
    if __sensors:
        processes = []
        parent_conn, child_conn = mp.Pipe()
        sensor_queue = mp.Queue()
        for s in __sensors:
            # Sensor process
            p = mp.Process(target=__sensor,
                           args=(sensor_queue, s, sensor_delay, ))
            processes.append(p)
            p.start()
        map(lambda p: p.join(), processes)
        # Aggregator process
        p = mp.Process(target=__aggregator,
                       args=(sensor_queue, aggregator_delay, publishers, ))
        processes.append(p)
        p.start()
        p.join()


def __sensor(queue, sensor, delay):
    try:
        while True:
            sleep(delay/1000)
            queue.put(sensor.get())
    except KeyboardInterrupt:
        pass


def __aggregator(queue, delay, publishers):
    try:
        for pub in publishers:
            pub.connect()
        device_data = {}
        init_timestamp = int((time() + 0.5) * 1000)
        while True:
            for sensor_id, sensor_value in iter(queue.get, None):
                timestamp = int((time() + 0.5) * 1000)
                if (timestamp - init_timestamp) >= delay:
                    for pub in publishers:
                        topic = pub.get_connection_data(KEY_PUB_TOPIC)
                        if topic is None:
                            topic = DEFAULT_PUB_TOPIC
                        device_id = pub.get_connection_data(KEY_DEVICE_ID)
                        if device_id is None:
                            device_id = DEFAULT_DEVICE_ID
                        device_data = json.dumps({device_id: {
                                           "timestamp": timestamp,
                                           "sensors": __agg_dictionary}},
                                          sort_keys=True)
                        pub.publish(topic, device_data)
                    init_timestamp = int((time() + 0.5) * 1000)
                    __agg_dictionary.clear()
                sensor_data = {sensor_id: {"timestamp": timestamp,
                               "value": sensor_value}}
                __agg_dictionary.append(sensor_data)
    except KeyboardInterrupt:
        pass
