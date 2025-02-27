from abc import ABC, abstractmethod

from src.core.category.domain.category import Category


class CategoryRepository(ABC):
    """
    Interface for a category repository.
    """

    @abstractmethod
    def save(self, category):
        """
        Save a category to the repository.

        Args:
            category (Category): The category to be saved.
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id) -> Category | None:
        """
        Retrieve a category by its ID from the repository.

        Args:
            id (uuid.UUID): The ID of the category to be retrieved.

        Returns:
            Category: The category with the given ID, or None if it doesn't exist.
        """
        raise NotImplementedError
