from abc import ABC, abstractmethod
from typing import List

from src.core._shared.events.event import Event


class AbstractMessageBus(ABC):
    """
    Abstract base class for a message bus.
    """

    @abstractmethod
    def handle(self, events: List[Event]) -> None:
        """
        Handle the given events.

        Args:
            events (List[Event]): The events to handle.
        """

        raise NotImplementedError
