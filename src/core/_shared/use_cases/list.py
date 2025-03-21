from dataclasses import dataclass, field
from typing import Generic, List, TypeVar

from src.config import DEFAULT_PAGE_SIZE

T = TypeVar("T")
RequestT = TypeVar("RequestT")


@dataclass
class ListRequest:
    """
    Represents the request parameters for listing entities.
    """

    order_by: str = "id"
    current_page: int = 1


@dataclass
class ListResponseMeta:
    """
    Represents the metadata of a list output.
    """

    current_page: int
    per_page: int
    total: int


@dataclass
class ListResponse:
    """
    Represents the response of listing entities.
    """

    data: List[T]  # type: ignore
    meta: ListResponseMeta = field(default_factory=ListResponseMeta)  # type: ignore


class ListUseCase(Generic[T, RequestT]):
    """
    Use case to list and sort entities based on the request parameters.
    """

    def __init__(self, repository):
        """
        Initialize the ListUseCase use case.

        Args:
            repository: The repository of the entities to be listed.
        """

        self.repository = repository

    def execute(self, request: RequestT) -> ListResponse:
        """
        Executes the use case to list and sort entities based on the request parameters.

        Args:
            request (RequestT): The request object containing sorting and pagination details.

        Returns:
            dict: A dictionary containing the paginated data and metadata information, including
                current page, items per page, and total number of entities.
        """

        entity = self.repository.list()
        sorted_entity = sorted(
            entity,
            key=lambda entity: getattr(
                entity,
                request.order_by,  # type: ignore
            ),
        )

        page_offset = (request.current_page - 1) * getattr(  # type: ignore
            request,
            "page_size",
            DEFAULT_PAGE_SIZE,
        )
        entity_page = sorted_entity[page_offset : page_offset + DEFAULT_PAGE_SIZE]

        return {
            "data": entity_page,
            "meta": ListResponseMeta(
                current_page=request.current_page,  # type: ignore
                per_page=DEFAULT_PAGE_SIZE,
                total=len(sorted_entity),
            ),
        }
