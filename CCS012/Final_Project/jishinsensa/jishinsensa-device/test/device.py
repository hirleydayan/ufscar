#!/usr/bin/env python3
"""Device small test program."""
import configparser
import jishinsensa.services.device as device
import getopt
import logging
import sys

from protocols.mqtt import MQTT
from jishinsensa.services.device.sensors import GPS
from jishinsensa.services.device.sensors import Lux
from jishinsensa.services.device.sensors import Temperature
from jishinsensa.services.device.sensors import Tilt


LOG_STR = '[%(asctime)s][%(name)s][%(levelname).3s] : %(message)s'

if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(LOG_STR)
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    options, remainder = getopt.getopt(sys.argv[1:],
                                       'c:s:', ['config',
                                                'section'])
    try:
        sections = []
        gps_file = None
        for opt, arg in options:
            if opt in ('-c', '--config'):
                cfg_file = arg
            elif opt in ('-s', '--section'):
                sections = [x.strip() for x in arg.split(',')]

        logger.info("Started")
        logger.info("Config: %s" % cfg_file)
        logger.info("Sections: %s" % sections)

        config = configparser.ConfigParser()
        config.read(cfg_file)
        connection_data = {}
        publishers = []

        for s in sections:
            connection_data = dict(config.items(s))
            publishers.append(MQTT(connection_data))

        device.add_sensor(Temperature())
        device.add_sensor(Tilt())
        device.add_sensor(Lux())

        if "settings" in config:
            settings = config["settings"]
            if "gps_data" in settings:
                logger.info("Simulated GPS Data: %s" % settings["gps_data"])
                with open(settings["gps_data"], encoding="utf-8") as file:
                    coordinates = file.readlines()
                    coordinates = [x.strip() for x in coordinates]
                device.add_sensor(GPS(coordinates))
            ts = 10000
            ta = 15000
            if "sensor_reading_delay" in settings:
                logger.info("Sensor Reading Delay: %s" %
                            settings["sensor_reading_delay"])
                ts = int(settings["sensor_reading_delay"])
            if "aggregation_delay" in settings:
                logger.info("Aggregation Delay: %s" %
                            settings["aggregation_delay"])
                ta = int(settings["aggregation_delay"])

        device.run(ts, ta, publishers)
    except KeyboardInterrupt:
        logger.info("Finished")
        sys.exit(0)
