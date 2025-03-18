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
