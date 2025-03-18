import uuid
from dataclasses import dataclass

from src.core.cast_member.application.exceptions import CastMemberNotFound
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


class DeleteCastMember:
    def __init__(self, repository: CastMemberRepository):
        """
        Initialize the DeleteCastMember use case.

        Args:
            repository (CastMemberRepository): The cast member repository.
        """

        self.repository = repository

    @dataclass
    class Input:
        """
        Input data for the DeleteCastMember use case.
        """

        id: uuid.UUID

    @dataclass
    class Output:
        """
        Output data for the DeleteCastMember use case.
        """

    def execute(self, input: Input) -> None:
        """
        Execute the DeleteCastMember use case.

        Args:
            input (Input): The input for the use case.

        Returns:
            Output: The output of the use case.
        """

        cast_member = self.repository.get_by_id(input.id)

        if cast_member is None:
            raise CastMemberNotFound(f"CastMember with ID {input.id} not found")

        self.repository.delete(cast_member_id=input.id)
