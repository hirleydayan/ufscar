#!/usr/bin/env python3
"""Device small test program."""
import configparser
import jishinsensa.services.device as device
import jishinsensa.services.platforms as ptf
import getopt
import sys

from jishinsensa.services.device.sensors import Tilt
from jishinsensa.services.device.sensors import Temperature
from jishinsensa.services.device.sensors import Lux


def get_config(config_file):
    """Get config."""
    config = configparser.ConfigParser()
    config.read(config_file)
    return config


if __name__ == '__main__':
    options, remainder = getopt.getopt(sys.argv[1:], 'c:s:', ['config=',
                                                              'section='])
    try:
        print ("Started")

        sections = []
        for opt, arg in options:
            if opt in ('-c', '--config'):
                cfg_file = arg
            elif opt in ('-s', '--section'):
                sections = [x.strip() for x in arg.split(',')]

        config = get_config(config_file=cfg_file)
        connection_data = {}
        publishers = []
        for s in sections:
            connection_data = dict(config.items(s))
            publishers.append(ptf.MQTT(connection_data))
        device.add_sensor(Temperature())
        device.add_sensor(Tilt())
        device.add_sensor(Lux())
        device.run(5000, 15000, publishers)
    except KeyboardInterrupt:
        sys.exit(0)
