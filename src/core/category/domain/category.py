from dataclasses import dataclass

from src.core._shared.domain.entity import AbstractEntity


@dataclass
class Category(AbstractEntity):
    """
    Represents a category of movies.
    """

    name: str
    description: str = ""
    is_active: bool = True

    def __post_init__(self):
        """
        Validate the category after it is created.

        This method is called automatically after the category is created.
        It validates the category's name and description.
        """

        self.validate()

    def __str__(self):
        """
        Return a human-readable string representation of the category.

        Returns:
            str: A human-readable string representation of the category.
        """
        return f"Category({self.name} - {self.description} ({self.is_active}))"

    def __repr__(self):
        """
        Return an unambiguous string representation of the category for debugging.

        Returns:
            str: An unambiguous string representation of the category.
        """

        return f"<Category {self.name} ({self.id})>"

    def validate(self):
        """
        Validate the category's name.

        Raises:
            ValueError: If the name is empty or longer than 255 characters.
        """

        if not self.name:
            # raise ValueError("Name cannot be empty")
            self.notification.add_error("Name cannot be empty")

        if len(self.name) > 255:
            # raise ValueError("Name must have less then 256 characters")
            self.notification.add_error("Name must have less then 256 characters")

        if len(self.description) > 1024:
            self.notification.add_error(
                "Description must have less then 1024 characters"
            )

        if self.notification.has_errors:
            raise ValueError(self.notification.messages)

    def update_category(self, name: str, description: str):
        """
        Update the name and description of the category.

        Args:
            name (str): The new name of the category.
            description (str): The new description of the category.
        """

        self.name = name
        self.description = description
        self.validate()

    def activate(self):
        """
        Activate the category.
        """

        self.is_active = True
        self.validate()

    def deactivate(self):
        """
        Deactivate the category.
        """

        self.is_active = False
        self.validate()
