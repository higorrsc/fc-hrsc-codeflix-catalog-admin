import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List

from src.core._shared.domain.notification import Notification
from src.core._shared.events.abstract_message_bus import AbstractMessageBus
from src.core._shared.events.event import Event
from src.core._shared.events.message_bus import MessageBus


@dataclass(kw_only=True)
class AbstractEntity(ABC):
    """
    Abstract base class for entities
    """

    id: uuid.UUID = field(default_factory=uuid.uuid4)
    notification: Notification = field(default_factory=Notification, init=False)
    events: List[Event] = field(default_factory=list, init=False)
    message_bus: AbstractMessageBus = field(default_factory=MessageBus, init=True)

    def __eq__(self, other):
        """
        Check if two entities are equal.

        Two entities are considered equal if they have the same ID.

        Args:
            other (object): The object to compare with.

        Returns:
            bool: True if the two entities are equal, False otherwise.
        """

        if not isinstance(other, self.__class__):
            return False

        return self.id == other.id

    @abstractmethod
    def validate(self):
        """
        Validate the entity.

        This method should be implemented in the concrete subclasses to validate
        the entity's state. It should raise a ValueError if the entity is in an
        invalid state.

        Raises:
            ValueError: If the entity is in an invalid state.
        """

        raise NotImplementedError

    def dispatch(self, event: Event) -> None:
        """
        Dispatch the given event.

        This method adds the given event to the entity's events list and calls the
        message bus's handle method with the events list.

        Args:
            event (Event): The event to dispatch.
        """

        self.events.append(event)
        self.message_bus.handle(self.events)
