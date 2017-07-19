"""Dragonboard sensors module."""
# import platform
# import re

TARGET_ID = "qcom"


class GPS():
    """Tilt sensor."""

    # Tilt('GPIO-C')
    def __init__(self, id, simulated_coordinates=None):
        """Init tilt sensor."""
        if id is None:
            raise ValueError("id must not be None")

        self.id = id

        # if re.search(TARGET_ID, platform.platform()):
        # TODO: GPS code for device has to be added
        #    pass
        # else:
        if simulated_coordinates is not None:
            self.coordinates_list = simulated_coordinates
            self.coord_idx = 0
            self.coord_max = len(self.coordinates_list) - 1

    def get_id(self):
        """Get sensor ID."""
        return self.id

    def get_coordinates(self):
        """Get tilt."""
        # if re.search(TARGET_ID, platform.platform()):
        # TODO: GPS code for device has to be added
        coordinates = None
        # else:
        if self.coordinates_list:
            if self.coord_idx > self.coord_max:
                self.coord_idx = 0
            coordinates = self.coordinates_list[self.coord_idx]
            self.coord_idx += 1
        return coordinates
