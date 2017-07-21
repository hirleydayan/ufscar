"""IBM Watson IoT Platform."""
import ibmiotf.device
import sys

from random import randint
from time import sleep

# Authentication key value
options = {"org": "v6tb44",
           "type": "ufscar_dragonboard",
           "id": "ufscar_db_02",
           "auth-method": "token",
           "auth-token": "BCJE@*sJjw0BKP_JBH"
           }


def connect():
    """Connect to IBM Watson IoT Platform."""
    try:
        client = ibmiotf.device.Client(options)
    except ibmiotf.ConnectionException:
        return None
    client.connect()
    return client


def puslish(client, data):
    """Publish data to IBM Watson IoT Platform."""
    if client is not None:
        print("Publishing: %s" % data)
        client.publishEvent("status", "json", data)
        return True
    else:
        return False


if __name__ == '__main__':
    try:
        client = connect()
        while True:
            data = {"temperature": randint(0, 100)}
            if not puslish(client, data):
                print("Could not connect to IBM Watson IoT Platform")
                sys.exit(0)
            sleep(5)

    except KeyboardInterrupt:
        pass
    else:
        client.disconnect()
    sys.exit(0)
