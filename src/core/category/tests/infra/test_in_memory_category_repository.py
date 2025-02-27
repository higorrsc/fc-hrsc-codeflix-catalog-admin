import uuid

from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
)


class TestSave:
    """
    Test cases for the in-memory category repository.
    """

    def test_can_save_category(self):
        """
        Test that a category can be saved to the in-memory repository.

        This test verifies that the `save` method of the `InMemoryCategoryRepository`
        successfully adds a `Category` instance to its internal category list.
        """
        repository = InMemoryCategoryRepository()
        category = Category(name="Action", description="Action movies")
        repository.save(category)
        assert category in repository.categories
        assert len(repository.categories) == 1
        assert repository.categories[0] == category


class TestGetById:
    """
    Test cases for the in-memory category repository.
    """

    def test_can_get_category_by_id(self):
        """
        Test that a category can be retrieved from the in-memory repository by its ID.

        This test verifies that the `get_by_id` method of the `InMemoryCategoryRepository`
        returns the correct `Category` instance when given a valid category ID.
        """
        repository = InMemoryCategoryRepository()
        category = Category(name="Action", description="Action movies")
        repository.save(category)
        retrieved_category = repository.get_by_id(category.id)
        assert retrieved_category == category

    def test_not_found_category_by_id(self):
        """
        Test that None is returned when a category is not found in the in-memory
        repository by its ID.

        This test verifies that the `get_by_id` method of the `InMemoryCategoryRepository`
        returns None when a category with the given ID is not found.
        """
        repository = InMemoryCategoryRepository()
        retrieved_category = repository.get_by_id(
            uuid.UUID("d5a9c8f0-6a8d-4a9d-9c4b-9d4a8b9c4d5a")
        )
        assert retrieved_category is None
