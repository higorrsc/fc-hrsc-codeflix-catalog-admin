from abc import ABC, abstractmethod

from src.core._shared.events.event import Event


class EventDispatcher(ABC):
    """
    Abstract base class for an event dispatcher.
    """

    @abstractmethod
    def dispatch(self, event: Event) -> None:
        """
        Dispatches the given event to the corresponding event handler.

        Args:
            event (Event): The event to dispatch.

        Raises:
            NotImplementedError: If the method has not been implemented.
        """

        raise NotImplementedError
