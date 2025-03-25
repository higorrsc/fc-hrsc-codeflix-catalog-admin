import uuid
from dataclasses import dataclass

from src.core._shared.application.use_cases.list import (
    ListRequest,
    ListResponse,
    ListUseCase,
)
from src.core.cast_member.domain.cast_member import CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


@dataclass
class CastMemberOutput:
    """
    Output for the ListCastMember use case
    """

    id: uuid.UUID
    name: str
    type: CastMemberType


class ListCastMember(ListUseCase):
    """
    List all cast members
    """

    def __init__(self, repository: CastMemberRepository):
        """
        Initialize the ListCastMember use case.

        Args:
            repository (CastMemberRepository): The cast member repository.
        """

        super().__init__(repository)

    def execute(self, request: ListRequest) -> ListResponse:
        """
        Executes the ListCastMember use case to list cast members based on request parameters.

        Args:
            request (ListRequest): The request object containing sorting and pagination details.

        Returns:
            ListResponse: A response containing the list of cast members and pagination metadata.
        """

        return super().execute(request)
