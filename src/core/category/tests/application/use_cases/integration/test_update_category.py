from src.core.category.application.use_cases.update_category import (
    UpdateCategory,
    UpdateCategoryRequest,
)
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
)


class TestUpdateCategory:
    """
    Test the update_category function
    """

    def test_can_update_category_name_and_description(self):
        """
        When calling update_category() to change the name and description of an existing category,
        the category's name and description are updated.

        This test verifies that the `update_category` use case successfully updates
        the name and description of the category in the repository.
        """
        category = Category(
            name="Action",
            description="Action movies",
        )

        repository = InMemoryCategoryRepository()
        repository.save(category)

        use_case = UpdateCategory(repository)
        request = UpdateCategoryRequest(
            id=category.id,
            name="Adventure",
            description="Adventure movies",
        )

        use_case.execute(request)
        updated_category = repository.get_by_id(category.id)

        assert updated_category.name == "Adventure"
        assert updated_category.description == "Adventure movies"
