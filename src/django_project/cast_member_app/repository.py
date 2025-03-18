import uuid
from typing import List

from src.core.cast_member.domain.cast_member import CastMember
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.django_project.cast_member_app.models import CastMember as CastMemberModel


class DjangoORMCastMemberRepository(CastMemberRepository):
    """
    Django ORM implementation for a cast member repository.
    """

    def __init__(self, cast_member_model: CastMemberModel | None = None):
        """
        Initialize the Django ORM Cast Member repository.

        Args:
            cast_member_model (CastMemberModel | None, optional): The CastMember model.
                Defaults to the CastMemberModel from the cast_member_app app.
        """
        self.cast_member_model = cast_member_model or CastMemberModel

    def save(self, cast_member: CastMember):
        """
        Save a cast member to the repository.

        Args:
            cast_member (CastMember): The cast member to be saved.
        """

        cast_member_data = {
            "id": cast_member.id,
            "name": cast_member.name,
            "type": cast_member.type,
        }

        self.cast_member_model.objects.create(**cast_member_data)

    def get_by_id(self, cast_member_id: uuid.UUID) -> CastMember | None:
        """
        Retrieve a cast member by its ID from the repository.

        Args:
            cast_member_id (uuid.UUID): The ID of the cast member to be retrieved.

        Returns:
            CastMember | None: The cast member with the given ID, or None if it doesn't exist.
        """

        try:
            cast_member = self.cast_member_model.objects.get(pk=cast_member_id)
            return CastMember(
                id=cast_member.id,
                name=cast_member.name,
                type=cast_member.type,  # type: ignore
            )
        except self.cast_member_model.DoesNotExist:
            return None

    def list(self) -> List[CastMember]:
        """
        List all cast members from the repository.

        Returns:
            list[CastMember]: A list of all cast members.
        """

        return [
            CastMember(
                id=cast_member.id,
                name=cast_member.name,
                type=cast_member.type,  # type: ignore
            )
            for cast_member in self.cast_member_model.objects.all()
        ]

    def delete(self, cast_member_id: uuid.UUID):
        """
        Delete a cast member by its ID from the repository.

        Args:
            cast_member_id (uuid.UUID): The ID of the cast member to be deleted.
        """

        self.cast_member_model.objects.filter(pk=cast_member_id).delete()

    def update(self, cast_member: CastMember):
        """
        Update a cast member in the repository.

        Args:
            cast_member (CastMember): The cast member to be updated.
        """

        raise NotImplementedError
