"""Dragonboard sensors module."""
import platform
import re
import random

TARGET_ID = "qcom"


class Tilt():
    """Tilt sensor."""

    # Tilt('GPIO-C')

    def __init__(self, gpio_name=None):
        """Init tilt sensor."""
        if gpio_name is None:
            return

        if re.search(TARGET_ID, platform.platform()):
            from libsoc_zero.GPIO import Tilt
            self.tilt = Tilt(gpio_name)

    def get_state(self):
        """Get tilt."""
        if re.search(TARGET_ID, platform.platform()):
            return self.tilt.is_tilted()
        else:
            return random.choice([True, False])
