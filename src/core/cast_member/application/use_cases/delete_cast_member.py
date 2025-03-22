from src.core._shared.application.use_cases.delete import DeleteRequest, DeleteUseCase
from src.core.cast_member.application.exceptions import CastMemberNotFound
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


class DeleteCastMember(DeleteUseCase):
    """
    Delete a cast member by its ID.
    """

    def __init__(self, repository: CastMemberRepository):
        """
        Initialize the DeleteCastMember use case.

        Args:
            repository (CastMemberRepository): The cast member repository.
        """

        super().__init__(
            repository=repository,
            not_found_exception=CastMemberNotFound,
            not_found_message="Cast member with ID {id} not found",
        )

    def execute(self, request: DeleteRequest) -> None:
        """
        Deletes a cast member by its ID.

        Args:
            request (DeleteRequest): The request with the ID of the cast member to be deleted.

        Raises:
            CastMemberNotFound: If the cast member is not found.
        """

        super().execute(request)
