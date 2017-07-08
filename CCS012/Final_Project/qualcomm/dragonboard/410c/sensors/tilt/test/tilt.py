"""Dragonboard sensors module."""
import qcom_db_410c.sensors.tilt as t
import platform
import re

TARGET_ID = "qcom"


if __name__ == '__main__':
    if re.search(TARGET_ID, platform.platform()):
        # D2
        tilt = t.Tilt('GPIO-C')
    else:
        tilt = t.Tilt()
    print("Tilted: %s" % ("true" if tilt.get_state() else "false"))
