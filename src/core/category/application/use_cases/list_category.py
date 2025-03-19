import uuid
from dataclasses import dataclass, field
from typing import List

from src.core.category.domain.category_repository import CategoryRepository


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

    order_by: str = "name"
    current_page: int = 1


@dataclass
class ListOutputMeta:
    """
    Represents the metadata of a list output.
    """

    current_page: int
    per_page: int
    total: int


@dataclass
class ListCategoryResponse:
    """
    Represents the response of listing a category by its ID.
    """

    data: List[CategoryOutput]
    meta: ListOutputMeta = field(default_factory=ListOutputMeta)  # type: ignore


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
        """
        Lists all categories.

        Args:
            request (ListCategoryRequest): The list category request.

        Returns:
            ListCategoryResponse: The list category response.
        """

        categories = self.repository.list()
        sorted_categories = sorted(
            [
                CategoryOutput(
                    id=category.id,
                    name=category.name,
                    description=category.description,
                    is_active=category.is_active,
                )
                for category in categories
            ],
            key=lambda category: getattr(category, request.order_by),
        )

        default_page_size = 2
        page_offset = (request.current_page - 1) * default_page_size
        categories_page = sorted_categories[
            page_offset : page_offset + default_page_size
        ]

        return ListCategoryResponse(
            data=categories_page,
            meta=ListOutputMeta(
                current_page=request.current_page,
                per_page=default_page_size,
                total=len(sorted_categories),
            ),
        )
