import uuid
from dataclasses import dataclass, field

from src.core._shared.entity import AbstractEntity


@dataclass
class Genre(AbstractEntity):
    """
    Represents a genre of movies.
    """

    name: str
    is_active: bool = True
    categories: set[uuid.UUID] = field(default_factory=set)

    def __post_init__(self):
        """
        Validate the genre after it is created.

        This method is called automatically after the genre is created.
        It validates the genre's name and description.
        """

        self.__validate()

    def __str__(self):
        """
        Return a human-readable string representation of the genre.

        Returns:
            str: A human-readable string representation of the genre.
        """

        return f"Genre({self.name} ({self.is_active}))"

    def __repr__(self):
        """
        Return an unambiguous string representation of the genre for debugging.

        Returns:
            str: An unambiguous string representation of the genre.
        """

        return f"<Genre {self.name} ({self.id})>"

    def __validate(self):
        """
        Validate the genre's name.

        Raises:
            ValueError: If the name is empty or longer than 255 characters.
        """

        if not self.name:
            # raise ValueError("Name cannot be empty")
            self.notification.add_error("Name cannot be empty")

        if len(self.name) > 255:
            # raise ValueError("Name must have less then 256 characters")
            self.notification.add_error("Name must have less then 256 characters")

        if self.notification.has_errors:
            raise ValueError(self.notification.messages)

    def change_name(self, name: str):
        """
        Update the name of the genre.

        Args:
            name (str): The new name of the genre.
        """

        self.name = name
        self.__validate()

    def activate(self):
        """
        Activate the genre.
        """

        self.is_active = True
        self.__validate()

    def deactivate(self):
        """
        Deactivate the genre.
        """

        self.is_active = False
        self.__validate()

    def add_category(self, category_id: uuid.UUID):
        """
        Add a category to the genre.

        Args:
            category_id (uuid.UUID): The ID of the category to add.
        """

        self.categories.add(category_id)
        self.__validate()

    def remove_category(self, category_id: uuid.UUID):
        """
        Remove a category from the genre.

        Args:
            category_id (uuid.UUID): The ID of the category to remove.
        """

        self.categories.remove(category_id)
        self.__validate()
