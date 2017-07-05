"""IBM Watson IoT Platform."""
import mqtt
import json
import sys
import temperature
import tilt

from time import sleep

ORG_ID = "v6tb44"
DEVICE_ID = "ufscar_db_02"
PASSWORD = "BCJE@*sJjw0BKP_JBH"
DEVICE_TYPE = "ufscar_dragonboard"

CLIENT_ID_FORMAT = "d:{org_id}:{type_id}:{device_id}"
USERNAME = "use-token-auth"
ENDPOINT_FORMAT = "{org_id}.messaging.internetofthings.ibmcloud.com"
EVENT_TOPIC_FORMAT = "iot-2/evt/{event_id}/fmt/json"
COMMAND_TOPIC_FORMAT = "iot-2/cmd/{command_id}/fmt/json"


if __name__ == '__main__':
    client_id = CLIENT_ID_FORMAT.format(org_id=ORG_ID, type_id=DEVICE_TYPE,
                                        device_id=DEVICE_ID)
    endpoint = ENDPOINT_FORMAT.format(org_id=ORG_ID)

    connection_data = {}
    connection_data["client_id"] = client_id
    connection_data["endpoint"] = endpoint
    connection_data["username"] = USERNAME
    connection_data["password"] = PASSWORD

    mqtt_client = mqtt.connect(connection_data)
    try:
        while True:
            event_topic = EVENT_TOPIC_FORMAT.format(event_id="dragon")
            # Temperature
            temp = temperature.get()
            data = json.dumps({"d": {"temperature": temp}})
            print("publishing: %s" % data)
            (rc, mid) = mqtt_client.publish(event_topic, data, qos=2)

            # Tilt
            t = tilt.get()
            if t == 1:
                data = json.dumps({"d": {"tilt": "tilted"}})
                print("publishing: tilted")
            else:
                data = json.dumps({"d": {"tilt": "normal"}})
                print("publishing: normal")

            (rc, mid) = mqtt_client.publish(event_topic, data, qos=2)

            sleep(5)

    except KeyboardInterrupt:
        pass
    else:
        mqtt_client.disconnect()
    sys.exit(0)
