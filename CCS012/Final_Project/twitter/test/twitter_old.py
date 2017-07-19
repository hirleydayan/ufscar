#!/usr/bin/env python3
"""Device small test program."""
import configparser
import getopt
import logging
import sys

from social.twitter import Twitter

LOG_STR = '[%(asctime)s][%(name)s][%(levelname).3s] : %(message)s'

def init_twitter_service():


if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(LOG_STR)
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    options, remainder = getopt.getopt(sys.argv[1:], 'c:', ['config'])
    try:
        sections = []
        gps_file = None
        for opt, arg in options:
            if opt in ('-c', '--config'):
                cfg_file = arg

        logger.info("Started")
        logger.info("Config: %s" % cfg_file)

        config = configparser.ConfigParser()
        config.read(cfg_file)

        if "twitter" not in config:
            print("No twitter settings in config file.")
            sys.exit(0)

        settings = dict(config.items("twitter"))

        if "fields" in settings:
            settings["fields"] =\
                [x.strip() for x in settings["fields"].split(',')]

        if "post_strings" in settings:
            settings["post_strings"] =\
                [x.strip() for x in settings["post_strings"].split(',')]
        else:
            settings["post_strings"] = ""

        print(settings["post_strings"])

        twitter = Twitter(settings)

    except KeyboardInterrupt:
        logger.info("Finished")
        sys.exit(0)
