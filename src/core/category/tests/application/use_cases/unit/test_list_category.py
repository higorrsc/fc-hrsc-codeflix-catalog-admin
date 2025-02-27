from unittest.mock import create_autospec

from src.core.category.application.use_cases.category_repository import (
    CategoryRepository,
)
from src.core.category.application.use_cases.list_category import (
    CategoryOutput,
    ListCategory,
    ListCategoryRequest,
    ListCategoryResponse,
)
from src.core.category.domain.category import Category


class TestListCategory:
    """
    Suite of tests for the `list_category` use case.
    """

    def test_when_no_categories_in_repository_then_return_empty_list(self):
        """
        Test that the `list_category` use case returns an empty list when no categories
        exist in the repository.

        This test verifies that the `list_category` use case successfully returns an
        empty `ListCategoryResponse` when the repository contains no categories.
        """

        mock_repository = create_autospec(CategoryRepository)
        mock_repository.list.return_value = []

        use_case = ListCategory(mock_repository)
        request = ListCategoryRequest()

        response = use_case.execute(request)

        assert response == ListCategoryResponse(data=[])
        assert mock_repository.list.called is True

    def test_when_categories_in_repository_then_return_list(self):
        """
        Test that the `list_category` use case returns a list of categories when categories
        exist in the repository.

        This test verifies that the `list_category` use case successfully returns a
        `ListCategoryResponse` containing a list of categories when the repository contains
        categories.
        """

        category_action = Category(
            name="Action",
            description="Action movies",
        )
        category_adventure = Category(
            name="Adventure",
            description="Adventure movies",
        )

        mock_repository = create_autospec(CategoryRepository)
        mock_repository.list.return_value = [
            category_action,
            category_adventure,
        ]

        use_case = ListCategory(mock_repository)
        request = ListCategoryRequest()

        response = use_case.execute(request)

        assert response == ListCategoryResponse(
            data=[
                CategoryOutput(
                    id=category_action.id,
                    name=category_action.name,
                    description=category_action.description,
                    is_active=category_action.is_active,
                ),
                CategoryOutput(
                    id=category_adventure.id,
                    name=category_adventure.name,
                    description=category_adventure.description,
                    is_active=category_adventure.is_active,
                ),
            ]
        )
        assert mock_repository.list.called is True
