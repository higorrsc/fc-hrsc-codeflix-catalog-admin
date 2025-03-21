import uuid
from dataclasses import dataclass, field

from src.core.cast_member.application.exceptions import InvalidCastMember
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


class CreateCastMember:
    """
    Create a new cast member
    """

    def __init__(self, repository: CastMemberRepository):
        """
        Initialize the CreateCastMember use case.

        Args:
            repository (CastMemberRepository): The cast member repository.
        """

        self.repository = repository

    @dataclass
    class Input:
        """
        Input for the CreateCastMember use case
        """

        name: str
        type: CastMemberType
        id: uuid.UUID = field(default_factory=uuid.uuid4)

    @dataclass
    class Output:
        """
        Output for the CreateCastMember use case
        """

        id: uuid.UUID

    def execute(self, input: Input) -> Output:
        """
        Create a new cast member.

        Args:
            input (Input): The input for this use case.

        Returns:
            Output: The output of this use case.

        Raises:
            InvalidCastMember: If the cast member is invalid.
        """

        try:
            cast_member = CastMember(
                id=input.id,
                name=input.name,
                type=input.type,
            )
        except ValueError as e:
            raise InvalidCastMember(e) from e

        self.repository.save(cast_member)
        return CreateCastMember.Output(id=cast_member.id)
