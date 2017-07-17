#!/usr/bin/env python3
"""Dragonboard sensors module."""
import qcom_db_410c.tilt as t
import platform
import re

TARGET_ID = "qcom"


if __name__ == '__main__':
    if re.search(TARGET_ID, platform.platform()):
        # D2
        tilt = t.Tilt("test_tilt_sensor", 'GPIO-C')
    else:
        tilt = t.Tilt("test_tilt_sensor")
    print("Tilted: %s" % ("true" if tilt.get_state() else "false"))
