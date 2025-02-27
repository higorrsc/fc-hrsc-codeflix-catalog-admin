from src.core.category.application.use_cases.delete_category import (
    DeleteCategory,
    DeleteCategoryRequest,
)
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
)


class TestDeleteCategory:
    def test_delete_category_from_repository(self):
        """
        When calling delete_category() with a valid category ID, it deletes the
        category from the repository.

        This test verifies that the `delete_category` use case successfully
        deletes a category by its ID from the repository.
        """
        category_action = Category(
            name="Action",
            description="Action movies",
        )
        category_horror = Category(
            name="Horror",
            description="Horror movies",
        )
        repository = InMemoryCategoryRepository(
            categories=[
                category_action,
                category_horror,
            ]
        )
        use_case = DeleteCategory(repository=repository)
        request = DeleteCategoryRequest(
            id=category_action.id,
        )

        assert repository.get_by_id(id=category_action.id) is not None
        use_case.execute(request)

        assert repository.get_by_id(id=category_action.id) is None
        assert len(repository.categories) == 1
        assert repository.categories[0].id == category_horror.id
