from unittest.mock import create_autospec

import pytest

from src.core.cast_member.application.use_cases.list_cast_member import (
    CastMemberOutput,
    ListCastMember,
)
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


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

    @pytest.fixture
    def mock_empty_repository(self) -> CastMemberRepository:
        """
        A fixture that returns an empty CastMemberRepository.
        """

        repository = create_autospec(CastMemberRepository)
        repository.list.return_value = []
        return repository

    @pytest.fixture
    def mock_repository(
        self,
        actor: CastMember,
        director: CastMember,
    ) -> CastMemberRepository:
        """
        A fixture that returns a CastMemberRepository with two CastMembers.
        """

        repository = create_autospec(CastMemberRepository)
        repository.list.return_value = [actor, director]
        return repository

    def test_when_no_cast_members_exist(
        self,
        mock_empty_repository: CastMemberRepository,
    ):
        """
        When there are no CastMembers in the repository, the use case should return an empty list.
        """

        use_case = ListCastMember(mock_empty_repository)
        output = use_case.execute(ListCastMember.Input())

        assert not output.data

    def test_when_cast_members_exist(
        self,
        mock_repository: CastMemberRepository,
        actor: CastMember,
        director: CastMember,
    ):
        """
        When there are CastMembers in the repository, the use case should return
        a list of CastMemberOutput objects.
        """

        use_case = ListCastMember(mock_repository)
        output = use_case.execute(ListCastMember.Input())

        assert len(output.data) == 2
        assert output == ListCastMember.Output(
            data=[
                CastMemberOutput(
                    id=actor.id,
                    name=actor.name,
                    type=actor.type,
                ),
                CastMemberOutput(
                    id=director.id,
                    name=director.name,
                    type=director.type,
                ),
            ]
        )
