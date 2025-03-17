import uuid

from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.infra.in_memory_cast_member_repository import (
    InMemoryCastMemberRepository,
)


class TestSave:
    """
    Test case for saving CastMembers in the in-memory repository.
    """

    def test_save_cast_member(self):
        """
        When saving a CastMember, it should be saved successfully.
        """

        repository = InMemoryCastMemberRepository()
        cast_member = CastMember(name="Robert Downey Jr.", type=CastMemberType.ACTOR)

        repository.save(cast_member)

        assert len(repository.cast_members) == 1
        assert cast_member in repository.list()


class TestGetById:
    """
    Test case for getting CastMembers by ID from the in-memory repository.
    """

    def test_get_cast_member_by_id(self):
        """
        When getting a CastMember by ID, it should return the correct CastMember.
        """

        cast_member_id = uuid.uuid4()
        cast_member = CastMember(
            name="Robert Downey Jr.",
            type=CastMemberType.ACTOR,
            id=cast_member_id,
        )

        repository = InMemoryCastMemberRepository()
        repository.save(cast_member)

        retrieved_cast_member = repository.get_by_id(cast_member_id)

        assert retrieved_cast_member == cast_member

    def test_get_non_existent_cast_member_by_id_returns_none(self):
        """
        When getting a non-existent CastMember by ID, it should return None.
        """

        repository = InMemoryCastMemberRepository()
        non_existent_cast_member_id = uuid.uuid4()

        retrieved_cast_member = repository.get_by_id(non_existent_cast_member_id)

        assert retrieved_cast_member is None


class TestList:
    """
    Test case for listing CastMembers from the in-memory repository.
    """

    def test_list_cast_members(self):
        """
        When listing CastMembers, it should return a list of CastMembers.
        """

        repository = InMemoryCastMemberRepository(
            cast_members=[
                CastMember(name="Robert Downey Jr.", type=CastMemberType.ACTOR),
                CastMember(name="Chris Evans", type=CastMemberType.ACTOR),
                CastMember(name="Clint Eastwood", type=CastMemberType.DIRECTOR),
            ]
        )

        cast_members = repository.list()

        assert len(cast_members) == 3
        assert cast_members[0].name == "Robert Downey Jr."
        assert cast_members[0].type == CastMemberType.ACTOR
        assert cast_members[1].name == "Chris Evans"
        assert cast_members[1].type == CastMemberType.ACTOR
        assert cast_members[2].name == "Clint Eastwood"
        assert cast_members[2].type == CastMemberType.DIRECTOR


class TestDelete:
    """
    Test case for deleting CastMembers from the in-memory repository.
    """

    def test_delete_cast_member(self):
        """
        When deleting a CastMember, it should be deleted successfully.
        """

        cast_member = CastMember(name="Robert Downey Jr.", type=CastMemberType.ACTOR)

        repository = InMemoryCastMemberRepository(
            cast_members=[
                cast_member,
                CastMember(name="Chris Evans", type=CastMemberType.ACTOR),
                CastMember(name="Clint Eastwood", type=CastMemberType.DIRECTOR),
            ]
        )

        repository.delete(cast_member.id)

        assert len(repository.cast_members) == 2
        assert cast_member not in repository.list()
        assert repository.cast_members[0].name == "Chris Evans"
        assert repository.cast_members[1].name == "Clint Eastwood"


class TestUpdate:
    """
    Test case for updating CastMembers in the in-memory repository.
    """

    def test_update_cast_member(self):
        """
        When updating a CastMember, it should be updated successfully.
        """

        cast_member = CastMember(name="Robert Downey Jr.", type=CastMemberType.ACTOR)

        repository = InMemoryCastMemberRepository()
        repository.save(cast_member)

        cast_member.name = "Chris Evans"
        repository.update(cast_member)

        updated_cast_member = repository.get_by_id(cast_member.id)

        assert updated_cast_member.name == "Chris Evans"  # type: ignore
        assert updated_cast_member.type == CastMemberType.ACTOR  # type: ignore

    def test_update_non_existent_cast_member_does_not_raises_exception(self):
        """
        When updating a non-existent CastMember, it should not raise an exception.
        """

        cast_member = CastMember(name="Robert Downey Jr.", type=CastMemberType.ACTOR)

        repository = InMemoryCastMemberRepository()
        repository.update(cast_member)

        assert len(repository.cast_members) == 0
        assert cast_member not in repository.list()
