import json

import pika

from src.core._shared.events.event import Event
from src.core._shared.events.event_dispatcher import EventDispatcher


class RabbitMQDispatcher(EventDispatcher):
    """
    Concrete implementation of a RabbitMQ event dispatcher.
    """

    def __init__(self, host: str = "localhost", queue: str = "videos.new") -> None:
        """
        Initialize the RabbitMQDispatcher.

        Args:
            host (str): The RabbitMQ host to connect to. Defaults to "localhost".
            queue (str): The name of the RabbitMQ queue to dispatch events to.
                Defaults to "videos.new".
        """

        self.host = host
        self.queue = queue
        self.connection = None
        self.channel = None

    def dispatch(self, event: Event) -> None:
        """
        Dispatch the given event to RabbitMQ.

        Args:
            event (Event): The event to dispatch.
        """

        if not self.connection:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=self.host)
            )
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.queue)

        self.channel.basic_publish(
            exchange="",
            routing_key=self.queue,
            body=json.dumps(event.payload),
        )
        print(f"Sent: {event} to queue {self.queue}")
