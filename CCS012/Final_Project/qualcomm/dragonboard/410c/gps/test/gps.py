#!/usr/bin/env python3
"""Dragonboard sensors module."""
import qcom_db_410c.gps as g
# import platform
# import re
from time import sleep

TARGET_ID = "qcom"


if __name__ == '__main__':
    # if re.search(TARGET_ID, platform.platform()):
    # D2
    #    gps = g.GPS("test_gps_sensor")
    # else:
    with open("coordinates.txt", encoding="utf-8") as file:
        coordinates = file.readlines()
        coordinates = [x.strip() for x in coordinates]
        gps = g.GPS("test_gps_sensor", coordinates)
        while True:
            print("GPS: %s" % gps.get_coordinates())
            sleep(2)
