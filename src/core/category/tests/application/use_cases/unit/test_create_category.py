import uuid
from unittest.mock import MagicMock

import pytest

from src.core.category.application.exceptions import InvalidCategoryData
from src.core.category.application.use_cases.category_repository import (
    CategoryRepository,
)
from src.core.category.application.use_cases.create_category import (
    CreateCategory,
    CreateCategoryRequest,
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
        mock_repository = MagicMock(CategoryRepository)
        use_case = CreateCategory(mock_repository)
        request = CreateCategoryRequest(
            name="Action",
            description="Action movies",
            is_active=True,  # default value
        )

        response = use_case.execute(request)

        assert response is not None
        assert isinstance(response.id, uuid.UUID)
        assert mock_repository.save.called is True

    def test_create_category_with_invalid_data(self):
        """
        When creating a Category with invalid data, it raises an InvalidCategoryData exception.

        A ValueError is raised if the name is empty or longer than 255 characters.
        """
        mock_repository = MagicMock(CategoryRepository)
        use_case = CreateCategory(mock_repository)
        request = CreateCategoryRequest(name="")
        with pytest.raises(
            InvalidCategoryData,
            match="Name cannot be empty",
        ) as exc_info:
            use_case.execute(request)

        assert exc_info.type is InvalidCategoryData
        assert str(exc_info.value.args[0]) == "Name cannot be empty"
