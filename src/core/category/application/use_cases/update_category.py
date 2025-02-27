import uuid
from dataclasses import dataclass

from src.core.category.application.exceptions import (
    CategoryNotFound,
    InvalidCategoryData,
)
from src.core.category.application.use_cases.category_repository import (
    CategoryRepository,
)


@dataclass
class UpdateCategoryRequest:
    """
    Request for updating a category
    """

    id: uuid.UUID
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None


class UpdateCategory:
    """
    Use case for updating a category
    """

    def __init__(self, repository: CategoryRepository):
        """
        Initialize the UpdateCategory use case.

        Args:
            repository (CategoryRepository): The category repository.
        """

        self.repository = repository

    def execute(self, request: UpdateCategoryRequest) -> None:
        """
        Updates a category.

        Args:
            request (UpdateCategoryRequest): The update category request.

        Raises:
            CategoryNotFound: If the category with the given ID does not exist.

        Returns:
            None: This use case does not return anything.
        """

        category = self.repository.get_by_id(category_id=request.id)

        if category is None:
            raise CategoryNotFound(f"Category with ID {request.id} not found")

        current_name = category.name
        current_description = category.description

        try:
            if request.name is not None:
                current_name = request.name

            if request.description is not None:
                current_description = request.description

            category.update_category(
                name=current_name,
                description=current_description,
            )

            if request.is_active is True:
                category.activate()

            if request.is_active is False:
                category.deactivate()
        except ValueError as err:
            raise InvalidCategoryData(err) from err

        self.repository.update(category)

        return None
