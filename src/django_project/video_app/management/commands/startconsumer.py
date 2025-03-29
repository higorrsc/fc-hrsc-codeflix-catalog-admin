from django.core.management.base import BaseCommand

from src.core.video.infra.video_converted_consumer import VideoConvertedRabbitMQConsumer


class Command(BaseCommand):
    """
    Command to start the RabbitMQ consumer to process the converted videos
    """

    help = "Start the RabbitMQ consumer to process the converted videos"

    def handle(self, *args, **kwargs) -> None:
        """
        Handles the command to start the RabbitMQ consumer.

        This method will create an instance of the VideoConvertedRabbitMQConsumer
        and call its start method to begin consuming messages from the queue.
        """

        consumer = VideoConvertedRabbitMQConsumer()
        consumer.start()
