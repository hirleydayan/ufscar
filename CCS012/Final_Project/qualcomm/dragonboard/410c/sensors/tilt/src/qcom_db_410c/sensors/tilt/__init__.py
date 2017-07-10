"""Dragonboard sensors module."""
import platform
import re
import random

TARGET_ID = "qcom"


class Tilt():
    """Tilt sensor."""

    # Tilt('GPIO-C')
    def __init__(self, id, gpio_name=None):
        """Init tilt sensor."""
        if id is None:
            raise ValueError("id must not be None")

        self.id = id

        if re.search(TARGET_ID, platform.platform()):
            if gpio_name is None:
                raise ValueError("gpio_name must not be None")

        if re.search(TARGET_ID, platform.platform()):
            from libsoc_zero.GPIO import Tilt
            self.tilt = Tilt(gpio_name)

    def get_id(self):
        """Get sensor ID."""
        return self.id

    def get_state(self):
        """Get tilt."""
        if re.search(TARGET_ID, platform.platform()):
            return self.tilt.is_tilted()
        else:
            return random.choice([True, False])
