import uuid
from unittest.mock import create_autospec

import pytest

from src.core.category.application.exceptions import CategoryNotFound
from src.core.category.application.use_cases.category_repository import (
    CategoryRepository,
)
from src.core.category.application.use_cases.update_category import (
    UpdateCategory,
    UpdateCategoryRequest,
)
from src.core.category.domain.category import Category


class TestUpdateCategory:
    """
    Test the update_category function
    """

    def test_update_category_name(self):
        """
        When calling update_category() to change the name of an existing category,
        the category's name is updated while its description remains unchanged.

        This test verifies that the `update_category` use case successfully updates
        the name of the category in the repository.
        """

        category_id = uuid.uuid4()
        category = Category(
            id=category_id,
            name="Action",
            description="Action movies",
            is_active=True,
        )
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = UpdateCategory(mock_repository)
        request = UpdateCategoryRequest(
            id=category.id,
            name="Adventure",
        )

        use_case.execute(request)

        assert category.name == "Adventure"
        assert category.description == "Action movies"
        mock_repository.update.assert_called_once_with(category)

    def test_update_category_description(self):
        """
        When calling update_category() to change the description of an existing category,
        the category's description is updated while its name remains unchanged.

        This test verifies that the `update_category` use case successfully updates
        the description of the category in the repository.
        """

        category_id = uuid.uuid4()
        category = Category(
            id=category_id,
            name="Action",
            description="Action movies",
            is_active=True,
        )
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = UpdateCategory(mock_repository)
        request = UpdateCategoryRequest(
            id=category.id,
            description="Adventure movies",
        )

        use_case.execute(request)

        assert category.name == "Action"
        assert category.description == "Adventure movies"
        mock_repository.update.assert_called_once_with(category)

    def test_can_deactivate_category(self):
        """
        When calling update_category() with is_active=False, the category is deactivated.

        This test verifies that the `update_category` use case successfully deactivates a
        category by its ID from the repository.
        """

        category_id = uuid.uuid4()
        category = Category(
            id=category_id,
            name="Action",
            description="Action movies",
            is_active=True,
        )
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = UpdateCategory(mock_repository)
        request = UpdateCategoryRequest(
            id=category.id,
            is_active=False,
        )

        use_case.execute(request)

        assert category.name == "Action"
        assert category.description == "Action movies"
        assert category.is_active is False
        mock_repository.update.assert_called_once_with(category)

    def test_can_activate_category(self):
        """
        When calling update_category() with a valid category ID and is_active=True,
        the category is activated.

        This test verifies that the `update_category` use case successfully
        activates a category by its ID from the repository.
        """
        category_id = uuid.uuid4()
        category = Category(
            id=category_id,
            name="Action",
            description="Action movies",
            is_active=False,
        )
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = UpdateCategory(mock_repository)
        request = UpdateCategoryRequest(
            id=category.id,
            is_active=True,
        )

        use_case.execute(request)

        assert category.name == "Action"
        assert category.description == "Action movies"
        assert category.is_active is True
        mock_repository.update.assert_called_once_with(category)

    def test_try_update_nonexistent_category(self):
        """
        When calling update_category() with a non-existent category ID,
        an exception is raised.

        This test verifies that the `update_category` use case raises a
        CategoryNotFound exception when trying to update a non-existent category.
        """
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = None

        use_case = UpdateCategory(mock_repository)
        request = UpdateCategoryRequest(
            id=uuid.uuid4(),
        )

        with pytest.raises(CategoryNotFound):
            use_case.execute(request)
