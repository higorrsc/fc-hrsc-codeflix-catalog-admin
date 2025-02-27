import uuid

import pytest

from src.core.category.application.exceptions import CategoryNotFound
from src.core.category.application.use_cases.get_category import (
    GetCategory,
    GetCategoryRequest,
    GetCategoryResponse,
)
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
)


class TestGetCategory:
    """
    Suite of tests for the get_category function.
    """

    def test_get_category_by_id(self):
        """
        When calling get_category_by_id() with a valid category ID, it returns
        a category with the same ID.

        The returned category is a `GetCategoryResponse` instance with the same
        attributes as the `Category` instance with the given ID.

        This test verifies that the `get_category_by_id` use case successfully
        retrieves a category by its ID from the repository.
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
        use_case = GetCategory(repository=repository)
        request = GetCategoryRequest(
            id=category_action.id,
        )

        response = use_case.execute(request)

        assert response == GetCategoryResponse(
            id=category_action.id,
            name=category_action.name,
            description=category_action.description,
            is_active=category_action.is_active,
        )

    def test_when_category_does_not_exist_then_raise_exception(self):
        """
        When calling get_category_by_id() with a category ID that does not
        exist in the repository, it raises a CategoryNotFound exception.

        This test verifies that the `get_category_by_id` use case raises a
        `CategoryNotFound` exception when the given category ID does not exist
        in the repository.
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
        use_case = GetCategory(repository=repository)
        not_found_id = uuid.uuid4()
        request = GetCategoryRequest(
            id=not_found_id,
        )

        with pytest.raises(CategoryNotFound):
            use_case.execute(request)
