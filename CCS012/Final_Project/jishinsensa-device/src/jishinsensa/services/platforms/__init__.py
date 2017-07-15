"""AWS IoT Platform."""
import protocols.mqtt as mqtt

PLATFORM_SERVICE = "mqtt"
PLATFORM_TOPIC = "topic"


class MQTT:
    """AWS platform."""

    def __init__(self, connection_data):
        """Constructor."""
        self.mqtt_client = None
        self.connection_data = connection_data

    def __del__(self):
        """Destructor."""
        if self.mqtt_client is not None:
            self.mqtt_client.disconnect()

    def get_connection_data(self, parameter=None):
        """Get connection data."""
        if parameter is None:
            return self.connection_data
        if parameter in self.connection_data:
            return self.connection_data[parameter]
        return None

    def connect(self):
        """Connect to AWS."""
        self.mqtt_client = mqtt.connect(self.connection_data)
        return self.mqtt_client

    def publish(self, topic, data, qos=0):
        """Publish method."""
        return self.mqtt_client.publish(topic, data)

    def subscribe(self, topic, data, qos=0):
        """Subscribe method."""
        return self.mqtt_client.subscribe(topic, qos)
