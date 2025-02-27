import uuid

from src.core.category.application.use_cases.category_repository import (
    CategoryRepository,
)
from src.core.category.domain.category import Category


class InMemoryCategoryRepository(CategoryRepository):
    """
    In memory category repository
    """

    def __init__(self, categories=None):
        """
        Initialize the in-memory category repository.

        Args:
            categories (list, optional): A list of categories to initialize the repository with.
            Defaults to an empty list if not provided.
        """

        self.categories = categories or []

    def save(self, category: Category) -> None:
        """
        Save a category to the in-memory repository.

        Args:
            category (Category): The category to be saved.
        """

        self.categories.append(category)

    def get_by_id(self, category_id: uuid.UUID) -> Category | None:
        """
        Retrieve a category by its ID from the in-memory repository.

        Args:
            id (uuid.UUID): The ID of the category to be retrieved.

        Returns:
            Category | None: The category with the given ID, or None if it doesn't exist.
        """

        for category in self.categories:
            if category.id == category_id:
                return category

        return None

    def delete(self, category_id: uuid.UUID) -> None:
        """
        Delete a category by its ID from the in-memory repository.

        Args:
            id (uuid.UUID): The ID of the category to be deleted.
        """

        self.categories = [
            category for category in self.categories if category.id != category_id
        ]

        return None

    def update(self, category: Category) -> None:
        """
        Update a category in the in-memory repository.

        Args:
            category (Category): The category to be updated.
        """

        for idx, cat in enumerate(self.categories):
            if cat.id == category.id:
                self.categories[idx] = category

        return None
