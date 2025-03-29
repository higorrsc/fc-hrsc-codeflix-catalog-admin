from abc import ABC, abstractmethod

from src.core._shared.events.event import Event


class AbstractHandler(ABC):
    """
    Abstract base class for a handler.
    """

    @abstractmethod
    def handle(self, event: Event) -> None:
        """
        Handle the given event.

        Args:
            event (Event): The event to be handled.
        """

        raise NotImplementedError
