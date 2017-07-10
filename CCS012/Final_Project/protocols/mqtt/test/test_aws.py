#!/usr/bin/env python3
"""AWS IoT Platform."""
import protocols.mqtt as mqtt
import json
import sys

from random import uniform
from time import sleep

awshost = "a2o3h5dcofelke.iot.us-west-2.amazonaws.com"
awsport = 8883
clientId = "ufscar_db_02"
thingName = "ufscar_db_02"
caPath = "rootCA.crt"
certPath = "cert.pem"
keyPath = "private.key"

if __name__ == '__main__':

    connection_data = {}
    connection_data["client_id"] = clientId
    connection_data["ca"] = caPath
    connection_data["certificate"] = certPath
    connection_data["private_key"] = keyPath
    connection_data["endpoint"] = awshost
    connection_data["port"] = awsport

    mqtt_client = mqtt.connect(connection_data)
    try:
        while True:
            # Temperature
            temp = uniform(20.0, 30.0)
            data = json.dumps({"d": {"temperature": temp}})
            print("publishing: %s" % temp)
            (rc, mid) = mqtt_client.publish("dragon", data, qos=1)
            sleep(5)

    except KeyboardInterrupt:
        pass
    else:
        mqtt_client.disconnect()
    sys.exit(0)
