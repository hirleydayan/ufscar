"""AWS IoT Platform."""
import mqtt
import json
import sys
import temperature
import tilt

from time import sleep

awshost = "a2o3h5dcofelke.iot.us-west-2.amazonaws.com"
awsport = 8883
clientId = "ufscar_db_02"
thingName = "ufscar_db_02"
caPath = "/home/linaro/aula_05/rootCA.crt"
certPath = "/home/linaro/aula_05/cert.pem"
keyPath = "/home/linaro/aula_05/private.key"

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
            temp = temperature.get()
            data = json.dumps({"d": {"temperature": temp}})
            print("publishing: %s" % temp)
            (rc, mid) = mqtt_client.publish("dragon", data, qos=1)

            # Tilt
            t = tilt.get()
            if t == 1:
                data = json.dumps({"d": {"tilt": "tilted"}})
                print("publishing: tilted")
            else:
                data = json.dumps({"d": {"tilt": "normal"}})
                print("publishing: normal")

            (rc, mid) = mqtt_client.publish("dragon", data, qos=1)

            sleep(5)

    except KeyboardInterrupt:
        pass
    else:
        mqtt_client.disconnect()
    sys.exit(0)
