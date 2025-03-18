import uuid

import pytest

from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.django_project.cast_member_app.models import CastMember as CastMemberModel
from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository


@pytest.mark.django_db
class TestSave:
    """
    Test case for saving CastMembers in the Django ORM repository.
    """

    def test_save_cast_member(self):
        """
        Test that a CastMember is saved correctly in the Django ORM repository.

        This test verifies that a CastMember instance is successfully saved
        to the database, and that the saved data matches the input data.
        It ensures the count of CastMemberModel objects increases by one,
        and the retrieved CastMember from the database has the correct
        attributes: id, name, and type.
        """

        cast_member = CastMember(name="John Doe", type=CastMemberType.ACTOR)
        repository = DjangoORMCastMemberRepository()

        assert CastMemberModel.objects.count() == 0
        repository.save(cast_member=cast_member)
        assert CastMemberModel.objects.count() == 1

        cast_member_from_db = CastMemberModel.objects.get()
        assert cast_member_from_db.id == cast_member.id
        assert cast_member_from_db.name == cast_member.name
        assert cast_member_from_db.type == cast_member.type


@pytest.mark.django_db
class TestGetById:
    """
    Test case for getting CastMembers by ID from the Django ORM repository.
    """

    def test_get_by_id_cast_member(self):
        """
        Test that a CastMember can be retrieved by its ID from the Django ORM repository.

        This test verifies that a CastMember instance can be retrieved from the
        database by its ID, and that the retrieved CastMember has the same
        attributes as the saved CastMember: id, name, and type.
        """

        cast_member = CastMember(name="John Doe", type=CastMemberType.ACTOR)
        repository = DjangoORMCastMemberRepository()
        repository.save(cast_member=cast_member)

        cast_member_from_db = repository.get_by_id(cast_member.id)
        assert cast_member_from_db.id == cast_member.id  # type: ignore
        assert cast_member_from_db.name == cast_member.name  # type: ignore
        assert cast_member_from_db.type == cast_member.type  # type: ignore

    def test_get_by_id_cast_member_not_found(self):
        """
        Test that attempting to retrieve a non-existent CastMember by ID
        from the Django ORM repository returns None.

        This test verifies that attempting to retrieve a CastMember by ID that
        does not exist in the database returns None.
        """

        cast_member_id = uuid.uuid4()
        repository = DjangoORMCastMemberRepository()
        cast_member_from_db = repository.get_by_id(cast_member_id)
        assert cast_member_from_db is None


@pytest.mark.django_db
class TestList:
    """
    Test case for listing CastMembers from the Django ORM repository.
    """

    def test_list_cast_members(self):
        """
        Test that the Django ORM repository correctly lists all saved CastMembers.

        This test saves three CastMembers to the repository, each with distinct names
        and types. It then verifies that the list method returns all three CastMembers
        with their correct attributes: name and type.
        """

        repository = DjangoORMCastMemberRepository()
        repository.save(
            cast_member=CastMember(
                name="Robert Downey Jr.",
                type=CastMemberType.ACTOR,
            ),
        )
        repository.save(
            cast_member=CastMember(
                name="Chris Evans",
                type=CastMemberType.ACTOR,
            ),
        )
        repository.save(
            cast_member=CastMember(
                name="Clint Eastwood",
                type=CastMemberType.DIRECTOR,
            ),
        )

        cast_members_from_db = repository.list()
        assert len(cast_members_from_db) == 3
        assert cast_members_from_db[0].name == "Robert Downey Jr."
        assert cast_members_from_db[0].type == CastMemberType.ACTOR
        assert cast_members_from_db[1].name == "Chris Evans"
        assert cast_members_from_db[1].type == CastMemberType.ACTOR
        assert cast_members_from_db[2].name == "Clint Eastwood"
        assert cast_members_from_db[2].type == CastMemberType.DIRECTOR


@pytest.mark.django_db
class TestDelete:
    """
    Test case for deleting CastMembers from the Django ORM repository.
    """

    def test_delete_cast_member(self):
        """
        When calling delete_cast_member() with a valid cast member ID, it deletes the
        cast member from the repository.

        The test verifies that when a valid ID is provided, the DeleteCastMember
        use case successfully deletes the cast member from the repository and calls
        the delete method on the repository once with the correct argument.
        """

        iron_man = CastMember(
            name="Robert Downey Jr.",
            type=CastMemberType.ACTOR,
        )
        captain_america = CastMember(
            name="Chris Evans",
            type=CastMemberType.ACTOR,
        )

        repository = DjangoORMCastMemberRepository()
        repository.save(cast_member=iron_man)
        repository.save(cast_member=captain_america)

        cast_members_from_db = repository.list()
        assert len(cast_members_from_db) == 2

        repository.delete(cast_member_id=iron_man.id)
        cast_members_from_db = repository.list()
        assert len(cast_members_from_db) == 1


@pytest.mark.django_db
class TestUpdate:
    """
    Test case for updating CastMembers in the Django ORM repository.
    """

    def test_update_cast_member(self):
        """
        When calling update_cast_member() with a valid cast member, it updates the
        cast member in the repository.

        The test verifies that when a valid cast member is provided, the
        UpdateCastMember use case successfully updates the cast member in the
        repository and calls the update method on the repository once with the
        correct argument.
        """

        cast_member = CastMember(name="Robert Downey Jr.", type=CastMemberType.ACTOR)
        repository = DjangoORMCastMemberRepository()
        repository.save(cast_member=cast_member)

        cast_member_from_db = repository.get_by_id(cast_member.id)
        assert cast_member_from_db.name == "Robert Downey Jr."  # type: ignore

        cast_member.name = "Chris Evans"
        repository.update(cast_member=cast_member)

        cast_member_from_db = repository.get_by_id(cast_member.id)
        assert cast_member_from_db.name == "Chris Evans"  # type: ignore
