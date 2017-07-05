"""Activity 3."""

import pika
import sys


def callback(ch, method, properties, body):
    """AMQP call back."""
    print(" [x] Received %r" % body)


if __name__ == '__main__':
    try:
        print("AMQP temp consumer started...")
        credenctials = pika.PlainCredentials('linaro', 'linaro')
        connection = pika.BlockingConnection(
                        pika.ConnectionParameters('192.168.123.2', 5672, '/',
                                                  credenctials))
        channel = connection.channel()
        channel.queue_declare(queue='hello_temp')
        channel.basic_consume(callback, queue='hello_temp', no_ack=True)
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Finished.")
        sys.exit(0)
