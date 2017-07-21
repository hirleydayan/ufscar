"""IBM Watson IoT Platform."""
import json
import paho.mqtt.client as mqtt
import sys

from random import randint
from time import sleep

IBM_ORG_ID = "v6tb44"
IBM_DEVICE_ID = "ufscar_db_02"
IBM_PASSWORD = "BCJE@*sJjw0BKP_JBH"
IBM_DEVICE_TYPE = "ufscar_dragonboard"


class AWS:
    """AWS IoT Platform connection variables."""

    pass


class IBM:
    """IBM Watson IoT Platform connection variables."""

    CLIENT_ID_FORMAT = "d:{org_id}:{type_id}:{device_id}"
    USERNAME = "use-token-auth"
    ENDPOINT_FORMAT = "{org_id}.messaging.internetofthings.ibmcloud.com"
    EVENT_TOPIC_FORMAT = "iot-2/evt/{event_id}/fmt/json"
    COMMAND_TOPIC_FORMAT = "iot-2/cmd/{command_id}/fmt/json"


def on_connect(mqttc, obj, flags, rc):
    """MQTT on connect callback."""
    print("connected: " + str(rc))


def on_message(mqttc, obj, msg):
    """MQTT on message callback."""
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


def on_publish(mqttc, obj, mid):
    """MQTT on publish callback."""
    print("message_id: " + str(mid))


def on_subscribe(mqttc, obj, mid, granted_qos):
    """MQTT on subscribe callback."""
    print("subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(mqttc, obj, level, string):
    """MQTT on log, for debugging, callback."""
    print(string)


def connect(client_id, endpoint, username=None, password=None, port=1883,
            keepalive=60):
    """MQTT connect."""
    mqtt_client = mqtt.Client(client_id)

    mqtt_client.on_connect = on_connect
    mqtt_client.on_publish = on_publish
    mqtt_client.on_subscribe = on_subscribe
    mqtt_client.on_log = on_log

    if username is not None and password is not None:
        mqtt_client.username_pw_set(username=username, password=password)
    mqtt_client.connect(host=endpoint, port=port, keepalive=keepalive)
    mqtt_client.loop_start()

    return mqtt_client


if __name__ == '__main__':
    ibm_client_id = IBM.CLIENT_ID_FORMAT.format(org_id=IBM_ORG_ID,
                                                type_id=IBM_DEVICE_TYPE,
                                                device_id=IBM_DEVICE_ID)
    ibm_endpoint = IBM.ENDPOINT_FORMAT.format(org_id=IBM_ORG_ID)
    ibm_mqtt_client = connect(client_id=ibm_client_id, endpoint=ibm_endpoint,
                              username=IBM.USERNAME, password=IBM_PASSWORD)
    try:
        while True:
            ibm_event_topic = IBM.EVENT_TOPIC_FORMAT.format(event_id="dragon")
            temp = randint(0, 100)
            data = json.dumps({"d": {"temperature": temp}})
            print("publishing: %s" % data)
            (rc, mid) = ibm_mqtt_client.publish(ibm_event_topic, data, qos=2)
            sleep(5)

    except KeyboardInterrupt:
        pass
    else:
        ibm_mqtt_client.disconnect()
    sys.exit(0)
