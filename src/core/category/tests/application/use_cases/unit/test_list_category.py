from unittest.mock import create_autospec

from src.config import DEFAULT_PAGE_SIZE
from src.core._shared.use_cases.list import ListRequest, ListResponse, ListResponseMeta
from src.core.category.application.use_cases.list_category import (
    CategoryOutput,
    ListCategory,
)
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository


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
        request = ListRequest()

        response: ListResponse = use_case.execute(request)

        assert response == {
            "data": [],
            "meta": ListResponseMeta(
                current_page=1,
                per_page=DEFAULT_PAGE_SIZE,
                total=0,
            ),
        }

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

        use_case = ListCategory(mock_repository)
        request = ListRequest(order_by="name")

        response: ListResponse = use_case.execute(request)

        assert response == {
            "data": [
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
            ],
            "meta": ListResponseMeta(
                current_page=1,
                per_page=DEFAULT_PAGE_SIZE,
                total=2,
            ),
        }

        assert mock_repository.list.called is True
