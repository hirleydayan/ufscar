#!/usr/bin/env python3
"""Device small test program."""
import configparser
import getopt
import logging
import sys

from social.twitter import Twitter
from protocols.mqtt import MQTT

LOG_STR = '[%(asctime)s][%(name)s][%(levelname).3s] : %(message)s'


def init_twitter_service(settings, publishers):
    """Init Twitter service."""
    if "fields" in settings:
        settings["fields"] =\
            [x.strip() for x in settings["fields"].split(',')]

    if "post_strings" in settings:
        settings["post_strings"] =\
            [x.strip() for x in settings["post_strings"].split(',')]
    else:
        settings["post_strings"] = ""

    Twitter(settings, publishers)


if __name__ == '__main__':
    logger = logging.getLogger()
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

        config = configparser.ConfigParser()
        config.read(cfg_file)

        if "settings" in config:
            if "logging" in config["settings"]:
                logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(LOG_STR)
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        logger.info("Started")
        logger.info("Config: %s" % cfg_file)
        logger.info("Sections: %s" % sections)
        if "twitter" not in config:
            print("No twitter settings in config file.")
            sys.exit(0)

        connection_data = {}
        publishers = []

        for s in sections:
            connection_data = dict(config.items(s))
            publishers.append(MQTT(connection_data))

        init_twitter_service(dict(config.items("twitter")), publishers)

    except KeyboardInterrupt:
        logger.info("Finished")
        sys.exit(0)
