import json

import pika


class VideoConvertedRabbitMQProducer:
    """
    A class for publishing messages to a RabbitMQ queue.
    """

    def __init__(
        self,
        host: str = "localhost",
        port: int = 5672,
        queue: str = "videos.converted",
    ) -> None:
        """
        Initialize the VideoConvertedRabbitMQProducer.

        Args:
            host (str): The RabbitMQ host to connect to. Defaults to "localhost".
            port (int): The RabbitMQ port to connect to. Defaults to 5672.
            queue (str): The name of the RabbitMQ queue to dispatch events to.
                Defaults to "videos.converted".
        """

        self.host = host
        self.queue = queue
        self.port = port
        self.connection = None
        self.channel = None
        self.start()

    def start(self) -> None:
        """
        Establish a connection to RabbitMQ and declare a queue.

        This method will block until it can connect to RabbitMQ and declare a queue.
        If an error occurs, it will print the error message to the console.
        """

        try:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    self.host,
                    self.port,
                ),
            )
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.queue)
        except Exception as e:
            print("Error connecting to RabbitMQ:", e)

    def publish(self, message: dict) -> None:
        """
        Publish a message to the RabbitMQ queue.

        This method publishes a given message to the specified RabbitMQ queue.
        If the RabbitMQ channel is not initialized, it prints an error message
        and exits the method. It also handles any exceptions that occur during
        the publishing process.

        Args:
            message (dict): The message to be published to the queue.
        """

        try:
            if not self.channel:
                print("RabbitMQ channel not initialized")
                return

            self.channel.basic_publish(
                exchange="",
                routing_key=self.queue,
                body=json.dumps(message),
            )
            print(f"Sent: {message} to queue {self.queue}")
        except Exception as e:
            print("Error sending message to RabbitMQ queue:", e)

    def close(self):
        """
        Close the connection to RabbitMQ if it is open.
        """

        if self.connection:
            self.connection.close()
