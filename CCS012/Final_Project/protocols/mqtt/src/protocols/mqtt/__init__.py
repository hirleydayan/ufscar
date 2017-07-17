"""MQTT Protocol."""
import logging
import paho.mqtt.client as mqtt
import ssl


class MQTT:
    """MQTT Class."""

    def __init__(self, connection_data):
        """Constructor."""
        self.mqttc = None
        self.logger = logging.getLogger()
        self.conn_data = connection_data

    def __del__(self):
        """Destructor."""
        if self.mqttc is not None:
            self.mqttc.disconnect()

    def on_connect(self, mqttc, obj, flags, rc):
        """MQTT on connect callback."""
        self.logger.debug("Connected: " + str(rc))

    def on_message(self, mqttc, obj, msg):
        """MQTT on message callback."""
        self.logger.debug(msg.topic + " " +
                          str(msg.qos) + " " + str(msg.payload))

    def on_publish(self, mqttc, obj, mid):
        """MQTT on publish callback."""
        self.logger.debug("Message ID: " + str(mid))

    def on_subscribe(self, mqttc, obj, mid, granted_qos):
        """MQTT on subscribe callback."""
        self.logger.debug("Subscribed: " + str(mid) + " " + str(granted_qos))

    def on_log(self, mqttc, obj, level, string):
        """MQTT on log, for debugging, callback."""
        self.logger.debug(string)

    def connect(self):
        """MQTT connect."""
        if type(self.conn_data) is not dict:
            return None

        if "client_id" in self.conn_data:
            self.mqttc = mqtt.Client(self.conn_data["client_id"])
        else:
            self.logger.error('Cannot connect. Missing "client_id".')
            return None

        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_publish = self.on_publish
        self.mqttc.on_subscribe = self.on_subscribe
        self.mqttc.on_log = self.on_log

        if "username" in self.conn_data and\
           "password" in self.conn_data:
            self.mqttc.username_pw_set(username=self.conn_data["username"],
                                       password=self.conn_data["password"])
        elif "ca" in self.conn_data and\
             "certificate" in self.conn_data and\
             "private_key" in self.conn_data:
            self.mqttc.tls_set(self.conn_data["ca"],
                               certfile=self.conn_data["certificate"],
                               keyfile=self.conn_data["private_key"],
                               cert_reqs=ssl.CERT_REQUIRED,
                               tls_version=ssl.PROTOCOL_TLSv1_2,
                               ciphers=None)

        if "endpoint" in self.conn_data:
            if "port" in self.conn_data:
                port = int(self.conn_data["port"])
            else:
                port = 1883

            if "keepalive" in self.conn_data:
                keepalive = self.conn_data["keepalive"]
            else:
                keepalive = 60

            self.mqttc.connect(host=self.conn_data["endpoint"],
                               port=port, keepalive=keepalive)
            self.mqttc.loop_start()
            # mqttc.loop_forever()
            return self.mqttc
        else:
            return None

        def publish(self, mqttc, topic, data, qos=0):
            """Publish method."""
            return self.mqttc.publish(topic, data)

        def subscribe(self, mqttc, topic, data, qos=0):
            """Subscribe method."""
            return self.mqttc.subscribe(topic, qos)

    def get_connection_data(self, parameter=None):
        """Get connection data."""
        if parameter is None:
            return self.conn_data
        if parameter in self.conn_data:
            return self.conn_data[parameter]
        return None

    def publish(self, topic, data, qos=0):
        """Publish method."""
        return self.mqttc.publish(topic, data)

    def subscribe(self, topic, data, qos=0):
        """Subscribe method."""
        return self.mqttc.subscribe(topic, qos)
