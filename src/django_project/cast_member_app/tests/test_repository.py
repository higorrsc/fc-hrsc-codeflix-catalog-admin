import uuid

import pytest

from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.django_project.cast_member_app.models import CastMember as CastMemberModel
from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository


@pytest.mark.django_db
class TestSave:
    def test_save_cast_member(self):
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
    def test_get_by_id_cast_member(self):
        cast_member = CastMember(name="John Doe", type=CastMemberType.ACTOR)
        repository = DjangoORMCastMemberRepository()
        repository.save(cast_member=cast_member)

        cast_member_from_db = repository.get_by_id(cast_member.id)
        assert cast_member_from_db.id == cast_member.id  # type: ignore
        assert cast_member_from_db.name == cast_member.name  # type: ignore
        assert cast_member_from_db.type == cast_member.type  # type: ignore

    def test_get_by_id_cast_member_not_found(self):
        cast_member_id = uuid.uuid4()
        repository = DjangoORMCastMemberRepository()
        cast_member_from_db = repository.get_by_id(cast_member_id)
        assert cast_member_from_db is None


@pytest.mark.django_db
class TestList:
    def test_list_cast_members(self):
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
    def test_delete_cast_member(self):
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
    def test_update_cast_member(self):
        cast_member = CastMember(name="Robert Downey Jr.", type=CastMemberType.ACTOR)
        repository = DjangoORMCastMemberRepository()
        repository.save(cast_member=cast_member)

        cast_member_from_db = repository.get_by_id(cast_member.id)
        assert cast_member_from_db.name == "Robert Downey Jr."  # type: ignore

        cast_member.name = "Chris Evans"
        repository.update(cast_member=cast_member)

        cast_member_from_db = repository.get_by_id(cast_member.id)
        assert cast_member_from_db.name == "Chris Evans"  # type: ignore
