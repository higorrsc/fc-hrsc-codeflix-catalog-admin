import uuid
from dataclasses import dataclass

from src.core.cast_member.application.exceptions import (
    CastMemberNotFound,
    InvalidCastMember,
)
from src.core.cast_member.domain.cast_member import CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


class UpdateCastMember:
    """
    Update a cast member.
    """

    def __init__(self, repository: CastMemberRepository):
        """
        Initialize the UpdateCastMember use case.

        Args:
            repository (CastMemberRepository): The cast member repository.
        """

        self.repository = repository

    @dataclass
    class Input:
        """
        Input for the UpdateCastMember use case.
        """

        id: uuid.UUID
        name: str
        type: CastMemberType

    @dataclass
    class Output:
        """
        Output for the UpdateCastMember use case.
        """

    def execute(self, input: Input) -> None:
        """
        Execute the UpdateCastMember use case.

        Args:
            input (Input): The input containing the ID, name, and type of the cast member to update.

        Raises:
            CastMemberNotFound: If no cast member is found with the given ID.
            InvalidCastMember: If the updated cast member is invalid.
        """

        cast_member = self.repository.get_by_id(input.id)
        if cast_member is None:
            raise CastMemberNotFound(f"CastMember with ID {input.id} not found")

        try:
            cast_member.update_cast_member(
                name=input.name,
                type=input.type,
            )
        except ValueError as e:
            raise InvalidCastMember(e) from e

        self.repository.update(cast_member)
