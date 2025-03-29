from abc import ABC, abstractmethod


class AbstractConsumer(ABC):
    """
    Abstract base class for a consumer.
    """

    @abstractmethod
    def on_message(self, message: bytes) -> None:
        """
        Handle an incoming message.

        This method should be implemented in the concrete subclasses to handle an
        incoming message. It should be called by the consumer's infrastructure when
        a message is received.

        Args:
            message (bytes): The message to be handled, as a byte string.
        """

        raise NotImplementedError

    @abstractmethod
    def start(self) -> None:
        """
        Start the consumer.

        This method should be implemented in the concrete subclasses to start the
        consumer's operation.
        """

        raise NotImplementedError

    @abstractmethod
    def stop(self) -> None:
        """
        Stop the consumer.

        This method should be implemented in the concrete subclasses to stop the
        consumer's operation gracefully.
        """

        raise NotImplementedError
