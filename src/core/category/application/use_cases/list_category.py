import uuid
from dataclasses import dataclass
from typing import List

from src.core.category.application.use_cases.category_repository import (
    CategoryRepository,
)


@dataclass
class CategoryOutput:
    """
    Represents the output of a category.
    """

    id: uuid.UUID
    name: str
    description: str
    is_active: bool


@dataclass
class ListCategoryRequest:
    """
    Represents the request to list a category by its ID.
    """


@dataclass
class ListCategoryResponse:
    """
    Represents the response of listing a category by its ID.
    """

    data: List[CategoryOutput]


class ListCategory:
    """
    List a category by its ID.
    """

    def __init__(self, repository: CategoryRepository):
        """
        Initialize the ListCategory use case.

        Args:
            repository (CategoryRepository): The category repository.
        """
        self.repository = repository

    def execute(self, request: ListCategoryRequest) -> ListCategoryResponse:
        categories = self.repository.list()

        return ListCategoryResponse(
            data=[
                CategoryOutput(
                    id=category.id,
                    name=category.name,
                    description=category.description,
                    is_active=category.is_active,
                )
                for category in categories
            ]
        )
