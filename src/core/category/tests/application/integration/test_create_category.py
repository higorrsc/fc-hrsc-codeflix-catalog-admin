import uuid

import pytest

from src.core.category.application.create_category import (
    CreateCategory,
    CreateCategoryRequest,
)
from src.core.category.application.exceptions import InvalidCategoryData
from src.core.category.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
)


class TestCreateCategory:
    """
    Suite of tests for the create_category function.
    """

    def test_create_category_with_valid_data(self):
        """
        When creating a Category with valid data, it returns a valid category ID.

        name, description and is_active are required and must have valid values.
        The category ID is an UUID.
        """
        repository = InMemoryCategoryRepository()
        use_case = CreateCategory(repository=repository)
        request = CreateCategoryRequest(
            name="Action",
            description="Action movies",
            is_active=True,  # default value
        )

        response = use_case.execute(request)

        assert response is not None
        assert isinstance(response.id, uuid.UUID)
        assert len(repository.categories) == 1
        assert repository.categories[0].name == "Action"
        assert repository.categories[0].description == "Action movies"
        assert repository.categories[0].is_active is True
        assert repository.categories[0].id == response.id

    def test_create_category_with_invalid_data(self):
        """
        When creating a Category with invalid data, it raises an InvalidCategoryData exception.

        A ValueError is raised if the name is empty or longer than 255 characters.
        """
        repository = InMemoryCategoryRepository()
        use_case = CreateCategory(repository)
        request = CreateCategoryRequest(name="")
        with pytest.raises(
            InvalidCategoryData,
            match="Name cannot be empty",
        ) as exc_info:
            use_case.execute(request)

        assert exc_info.type is InvalidCategoryData
        assert str(exc_info.value.args[0]) == "Name cannot be empty"
