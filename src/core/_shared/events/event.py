from abc import ABC
from dataclasses import asdict, dataclass
from typing import Dict, TypeVar


@dataclass(frozen=True)
class Event(ABC):
    """
    Abstract class representing an event.
    """

    @property
    def type(self) -> str:
        """
        Get the type of the event.

        Returns:
            str: The name of the event's class.
        """

        return self.__class__.__name__

    @property
    def payload(self) -> Dict:
        """
        Get the payload of the event.

        The payload is a dictionary containing all the attributes of the event.

        Returns:
            Dict: The payload of the event.
        """
        return asdict(self)

    def __str__(self) -> str:
        """
        Return a string representation of the event.

        The string representation is in the format
        "<event_type>: <event_payload>".

        Returns:
            str: A string representation of the event.
        """

        return f"{self.type}: {self.payload}"

    def __repr__(self) -> str:
        """
        Return a string representation of the event.

        Returns:
            str: A string representation of the event.
        """

        return self.__str__()


TEvent = TypeVar("TEvent", bound=Event)
