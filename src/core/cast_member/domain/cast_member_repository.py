import uuid
from abc import ABC, abstractmethod
from typing import List

from src.core.cast_member.domain.cast_member import CastMember


class CastMemberRepository(ABC):
    """
    Interface for a cast member repository.
    """

    @abstractmethod
    def save(self, cast_member: CastMember):
        """
        Save a cast member to the repository.

        Args:
            cast_member (CastMember): The cast member to be saved.
        """

        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, cast_member_id: uuid.UUID) -> CastMember | None:
        """
        Retrieve a cast member by its ID from the repository.

        Args:
            cast_member_id (uuid.UUID): The ID of the cast member to be retrieved.

        Returns:
            CastMember | None: The cast member with the given ID, or None if it doesn't exist.
        """

        raise NotImplementedError

    @abstractmethod
    def list(self) -> List[CastMember]:
        """
        List all cast members from the repository.

        Returns:
            list[CastMember]: A list of all cast members.
        """

        raise NotImplementedError

    @abstractmethod
    def delete(self, cast_member_id: uuid.UUID):
        """
        Delete a cast member by its ID from the repository.

        Args:
            cast_member_id (uuid.UUID): The ID of the cast member to be deleted.
        """

        raise NotImplementedError

    @abstractmethod
    def update(self, cast_member: CastMember):
        """
        Update a cast member in the repository.

        Args:
            cast_member (CastMember): The cast member to be updated.
        """

        raise NotImplementedError
