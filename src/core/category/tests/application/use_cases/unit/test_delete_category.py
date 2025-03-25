import uuid
from unittest.mock import create_autospec

import pytest

from src.core._shared.application.use_cases.delete import DeleteRequest
from src.core.category.application.exceptions import CategoryNotFound
from src.core.category.application.use_cases.delete_category import DeleteCategory
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository


class TestDeleteCategory:
    """
    Suite of tests for the `delete_category` use case.
    """

    def test_delete_category_from_repository(self):
        """
        When calling delete_category() with a valid category ID, it deletes the
        category from the repository.

        This test verifies that the `delete_category` use case successfully
        deletes a category by its ID from the repository.

        """
        category = Category("Action", "Action movies")
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = DeleteCategory(mock_repository)
        use_case.execute(DeleteRequest(id=category.id))

        mock_repository.delete.assert_called_once_with(category.id)

    def test_when_category_not_found_then_raise_exception(self):
        """
        When calling delete_category() with a category ID that does not exist in the
        repository, it raises a CategoryNotFound exception.

        This test verifies that the `delete_category` use case raises a
        `CategoryNotFound` exception when the given category ID does not exist in
        the repository.
        """

        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = None

        not_found_id = uuid.uuid4()
        use_case = DeleteCategory(mock_repository)

        with pytest.raises(
            CategoryNotFound,
            match=f"Category with ID {not_found_id} not found",
        ):
            use_case.execute(DeleteRequest(id=not_found_id))

        mock_repository.delete.assert_not_called()
        assert mock_repository.delete.called is False
