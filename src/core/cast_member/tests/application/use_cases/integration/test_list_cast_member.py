import pytest

from src.config import DEFAULT_PAGE_SIZE
from src.core._shared.application.use_cases.list import (
    ListRequest,
    ListResponse,
    ListResponseMeta,
)
from src.core.cast_member.application.use_cases.list_cast_member import ListCastMember
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.infra.in_memory_cast_member_repository import (
    InMemoryCastMemberRepository,
)


class TestListCastMember:
    """
    A class for testing the ListCastMember use case.
    """

    @pytest.fixture
    def actor(self) -> CastMember:
        """
        A fixture that returns a CastMember with the name "Robert Downey Jr." and type ACTOR.
        """

        return CastMember(
            name="Robert Downey Jr.",
            type=CastMemberType.ACTOR,
        )

    @pytest.fixture
    def director(self) -> CastMember:
        """
        A fixture that returns a CastMember with the name "Clint Eastwood" and type DIRECTOR.
        """

        return CastMember(
            name="Clint Eastwood",
            type=CastMemberType.DIRECTOR,
        )

    def test_when_no_cast_members_exist(self):
        """
        When there are no CastMembers in the repository, the use case should return an empty list.
        """

        empty_repository = InMemoryCastMemberRepository()
        use_case = ListCastMember(empty_repository)
        output: ListResponse = use_case.execute(ListRequest(order_by="name"))

        assert output == {
            "data": [],
            "meta": ListResponseMeta(
                current_page=1,
                per_page=DEFAULT_PAGE_SIZE,
                total=0,
            ),
        }

    def test_when_cast_members_exist(
        self,
        actor: CastMember,
        director: CastMember,
    ):
        """
        When there are CastMembers in the repository, the use case should return
        a list of CastMemberOutput objects.
        """

        repository = InMemoryCastMemberRepository(
            cast_members=[
                actor,
                director,
            ]
        )
        use_case = ListCastMember(repository)
        output: ListResponse = use_case.execute(ListRequest(order_by="name"))

        assert output == {
            "data": [
                director,
                actor,
            ],
            "meta": ListResponseMeta(
                current_page=1,
                per_page=DEFAULT_PAGE_SIZE,
                total=2,
            ),
        }
