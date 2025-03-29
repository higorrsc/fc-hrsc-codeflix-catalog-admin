from src.core._shared.events.event import Event
from src.core._shared.events.event_dispatcher import EventDispatcher


class RabbitMQDispatcher(EventDispatcher):
    """
    Concrete implementation of a RabbitMQ event dispatcher.
    """

    def __init__(self, queue_name: str = "videos.new") -> None:
        """
        Initialize the RabbitMQDispatcher.

        Args:
            queue_name (str): The name of the RabbitMQ queue to dispatch events to.
        """

        self.queue_name = queue_name

    def dispatch(self, event: Event) -> None:
        """
        Dispatch the given event to RabbitMQ.

        This method prints a message indicating that the event is being dispatched
        to RabbitMQ.

        Args:
            event (Event): The event to dispatch.
        """

        print(f"RabbitMQ Dispatching event: {event}")
