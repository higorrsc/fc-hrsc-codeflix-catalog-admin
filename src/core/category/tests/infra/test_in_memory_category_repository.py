from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
)


class TestInMemoryCategoryRepository:
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
