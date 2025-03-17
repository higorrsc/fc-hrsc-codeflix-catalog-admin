import uuid
from dataclasses import dataclass
from typing import List

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


class ListCastMember:
    """
    List all cast members
    """

    def __init__(self, repository: CastMemberRepository):
        """
        Initialize the ListCastMember use case.

        Args:
            repository (CastMemberRepository): The cast member repository.
        """

        self.repository = repository

    @dataclass
    class Input:
        """
        Input for the ListCastMember use case
        """

    @dataclass
    class Output:
        """
        Output for the ListCastMember use case
        """

        data: List[CastMemberOutput]

    def execute(self, input: Input) -> Output:
        """
        List all cast members

        Returns:
            ListCastMember.Output: A list of cast members
        """

        cast_members = self.repository.list()
        return ListCastMember.Output(
            data=[
                CastMemberOutput(
                    id=cast_member.id,
                    name=cast_member.name,
                    type=cast_member.type,
                )
                for cast_member in cast_members
            ]
        )
