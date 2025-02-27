from unittest.mock import create_autospec

from src.core.category.application.use_cases.category_repository import (
    CategoryRepository,
)
from src.core.category.application.use_cases.get_category import (
    GetCategory,
    GetCategoryRequest,
    GetCategoryResponse,
)
from src.core.category.domain.category import Category


class TestGetCategory:
    """
    Suite of tests for the get_category function.
    """

    def test_return_found_category(self):
        """
        When calling get_category_by_id() with a valid category ID, it returns
        a category with the same ID.

        The returned category is a `GetCategoryResponse` instance with the same
        attributes as the `Category` instance with the given ID.

        This test verifies that the `get_category_by_id` use case successfully
        retrieves a category by its ID from the repository.
        """
        category = Category(
            name="Action",
            description="Action movies",
        )
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category
        use_case = GetCategory(mock_repository)
        request = GetCategoryRequest(id=category.id)

        response = use_case.execute(request)

        assert response is not None
        assert isinstance(response, GetCategoryResponse)
        assert response == GetCategoryResponse(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active,
        )
        assert mock_repository.get_by_id.called is True
