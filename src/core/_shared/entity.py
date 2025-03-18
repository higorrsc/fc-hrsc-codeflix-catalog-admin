import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from src.core._shared.notification import Notification


@dataclass(kw_only=True)
class AbstractEntity(ABC):
    """
    Abstract base class for entities
    """

    id: uuid.UUID = field(default_factory=uuid.uuid4)
    notification: Notification = field(default_factory=Notification)

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
