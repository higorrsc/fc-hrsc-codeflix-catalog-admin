import uuid
from typing import List

from src.core.cast_member.domain.cast_member import CastMember
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


class InMemoryCastMemberRepository(CastMemberRepository):
    """
    An in-memory implementation of the CastMemberRepository interface.
    """

    def __init__(self, cast_members: List[CastMember] = None):  # type: ignore
        """
        Initialize the in-memory cast member repository.

        Args:
            cast_members (List[CastMember], optional): A list of cast members to
                initialize the repository with.
            Defaults to an empty list if not provided.
        """

        self.cast_members = cast_members or []

    def save(self, cast_member: CastMember):
        """
        Save a cast member to the repository.

        Args:
            cast_member (CastMember): The cast member to be saved.
        """

        self.cast_members.append(cast_member)

    def get_by_id(self, cast_member_id: uuid.UUID) -> CastMember | None:
        """
        Retrieve a cast member by its ID from the repository.

        Args:
            cast_member_id (uuid.UUID): The ID of the cast member to be retrieved.

        Returns:
            CastMember | None: The cast member with the given ID, or None if it doesn't exist.
        """

        for cast_member in self.cast_members:
            if cast_member.id == cast_member_id:
                return cast_member

        return None

    def list(self) -> List[CastMember]:
        """
        List all cast members from the repository.

        Returns:
            List[CastMember]: A list of all cast members.
        """

        return [cast_member for cast_member in self.cast_members]

    def delete(self, cast_member_id: uuid.UUID) -> None:
        """
        Delete a cast member by its ID from the repository.

        Args:
            cast_member_id (uuid.UUID): The ID of the cast member to be deleted.
        """

        cast_member = self.get_by_id(cast_member_id)

        if cast_member:
            self.cast_members.remove(cast_member)

    def update(self, cast_member: CastMember) -> None:
        """
        Update a cast member in the repository.

        Args:
            cast_member (CastMember): The cast member to be updated.
        """

        old_cast_member = self.get_by_id(cast_member.id)

        if old_cast_member:
            self.cast_members.remove(old_cast_member)
            self.cast_members.append(cast_member)
