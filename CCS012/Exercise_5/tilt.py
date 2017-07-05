"""Tilt sensor module."""
from libsoc_zero.GPIO import Tilt

tilt = Tilt('GPIO-C')


def get():
    """Get tilt."""
    if tilt.is_tilted():
        return 1
    else:
        return 0


if __name__ == '__main__':
    print("Tilted: %d" % get())
