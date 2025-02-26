import uuid


class Category:
    """
    Represents a category of movies.
    """

    def __init__(
        self,
        name: str,
        id: uuid.UUID = None,
        description: str = "",
        is_active: bool = True,
    ):
        """
        Initialize a new Category instance.

        Args:
            name (str): The name of the category.
            id (uuid.UUID, optional): The unique identifier for the category.
                If not provided, a new UUID will be generated. Defaults to an empty string.
            description (str, optional): A description of the category.
                Defaults to an empty string.
            is_active (bool, optional): Indicates whether the category is active.
                Defaults to True.
        """
        self.id = id or uuid.uuid4()
        self.name = name
        self.description = description
        self.is_active = is_active

        if len(self.name) > 255:
            raise ValueError("Name must have less then 256 characters")

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
