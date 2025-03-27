from dataclasses import dataclass
from enum import StrEnum

from src.core._shared.domain.entity import AbstractEntity


class CastMemberType(StrEnum):
    """
    Represents the type of a cast member.
    """

    ACTOR = "ACTOR"
    DIRECTOR = "DIRECTOR"


@dataclass()
class CastMember(AbstractEntity):
    """
    Represents a cast member of a movie.
    """

    name: str
    type: CastMemberType

    def __post_init__(self):
        """
        Validate the cast member after initialization.

        This method is called automatically after the cast member is created.
        It validates the cast member's name and type.
        """

        self.validate()

    def __str__(self) -> str:
        """
        Return a human-readable string representation of the cast member.

        Returns:
            str: A human-readable string representation of the cast member.
        """

        return f"CastMember({self.name} - {self.type})"

    def __repr__(self) -> str:
        """
        Return an unambiguous string representation of the cast member for debugging.

        Returns:
            str: An unambiguous string representation of the cast member.
        """

        return f"<CastMember {self.name} ({self.id})>"

    def __eq__(self, value: object) -> bool:
        """
        Check if two CastMember instances are equal.

        Two CastMember instances are considered equal if they have the same ID.

        Args:
            value (object): The object to compare with.

        Returns:
            bool: True if the two CastMember instances are equal, False otherwise.
        """

        if not isinstance(value, CastMember):
            return False

        return (
            self.id == value.id and self.name == value.name and self.type == value.type
        )

    def validate(self):
        """
        Validate the cast member.

        Raises:
            ValueError: If the name or type is empty.
            ValueError: If the name is longer than 255 characters.
        """

        if not self.name:
            self.notification.add_error("Name cannot be empty")

        if len(self.name) > 255:
            self.notification.add_error("Name must have less then 256 characters")

        if self.type not in CastMemberType:
            self.notification.add_error(
                "Type must be a valid CastMemberType: ACTOR or DIRECTOR"
            )

        if self.notification.has_errors:
            raise ValueError(self.notification.messages)

    def update_cast_member(self, name: str, type: CastMemberType):
        """
        Update the name and type of the cast member.

        Args:
            name (str): The new name of the cast member.
            type (CastMemberType): The new type of the cast member.

        Raises:
            ValueError: If the name or type is empty.
            ValueError: If the name is longer than 255 characters.
        """

        self.name = name
        self.type = type
        self.validate()
