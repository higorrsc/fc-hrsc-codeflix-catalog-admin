import uuid
from unittest.mock import create_autospec

import pytest

from src.core.cast_member.application.exceptions import (
    CastMemberNotFound,
    InvalidCastMember,
)
from src.core.cast_member.application.use_cases.update_cast_member import (
    UpdateCastMember,
)
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


class TestUpdateCastMember:
    """
    A class for testing the UpdateCastMember use case.
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
    def mock_repository(self, actor: CastMember) -> CastMemberRepository:
        """
        A fixture that returns a mock repository containing the actor CastMember.
        """

        repository = create_autospec(CastMemberRepository)
        repository.get_by_id.return_value = actor
        return repository

    @pytest.fixture
    def mock_empty_repository(self) -> CastMemberRepository:
        """
        A fixture that returns a mock repository with no CastMembers.
        """

        repository = create_autospec(CastMemberRepository)
        repository.get_by_id.return_value = None
        return repository

    def test_when_cast_member_is_found(
        self,
        actor: CastMember,
        mock_repository: CastMemberRepository,
    ):
        """
        When calling update_cast_member() with a valid cast member ID,
        it updates the cast member in the repository.
        """

        use_case = UpdateCastMember(mock_repository)
        use_case.execute(
            UpdateCastMember.Input(
                id=actor.id,
                name="John Doe",
                type=CastMemberType.DIRECTOR,
            )
        )

        mock_repository.update.assert_called_once_with(actor)  # type: ignore
        assert actor.name == "John Doe"
        assert actor.type == CastMemberType.DIRECTOR

    def test_when_cast_member_is_not_found(
        self,
        mock_empty_repository: CastMemberRepository,
    ):
        """
        When calling update_cast_member() with a non-existent cast member ID,
        it raises a CastMemberNotFound exception.
        """

        use_case = UpdateCastMember(mock_empty_repository)
        with pytest.raises(CastMemberNotFound):
            use_case.execute(
                UpdateCastMember.Input(
                    id=uuid.uuid4(),
                    name="John Doe",
                    type=CastMemberType.DIRECTOR,
                )
            )

    def test_when_cast_member_name_is_invalid(
        self,
        actor: CastMember,
        mock_repository: CastMemberRepository,
    ):
        """
        When calling update_cast_member() with a cast member name that is too long,
        it raises an InvalidCastMember exception with the message
        "Name must have less then 256 characters".
        """

        use_case = UpdateCastMember(mock_repository)
        with pytest.raises(InvalidCastMember) as exc_info:
            use_case.execute(
                UpdateCastMember.Input(
                    id=actor.id,
                    name="a" * 256,
                    type=CastMemberType.DIRECTOR,
                )
            )

        assert exc_info.type is InvalidCastMember
        assert str(exc_info.value) == "Name must have less then 256 characters"
        mock_repository.update.assert_not_called()  # type: ignore

    def test_when_cast_member_name_is_empty(
        self,
        actor: CastMember,
        mock_repository: CastMemberRepository,
    ):
        """
        When calling update_cast_member() with a cast member name that is empty,
        it raises an InvalidCastMember exception with the message "Name cannot be empty".
        """

        use_case = UpdateCastMember(mock_repository)
        with pytest.raises(InvalidCastMember) as exc_info:
            use_case.execute(
                UpdateCastMember.Input(
                    id=actor.id,
                    name="",
                    type=CastMemberType.DIRECTOR,
                )
            )

        assert exc_info.type is InvalidCastMember
        assert str(exc_info.value) == "Name cannot be empty"
        mock_repository.update.assert_not_called()  # type: ignore

    def test_when_cast_member_type_is_invalid(
        self,
        actor: CastMember,
        mock_repository: CastMemberRepository,
    ):
        """
        When calling update_cast_member() with a cast member type that is invalid,
        it raises an InvalidCastMember exception with the message
        "Type must be a valid CastMemberType: ACTOR or DIRECTOR".
        """

        use_case = UpdateCastMember(mock_repository)
        with pytest.raises(InvalidCastMember) as exc_info:
            use_case.execute(
                UpdateCastMember.Input(
                    id=actor.id,
                    name="John Doe",
                    type="",  # type: ignore
                )
            )

        assert exc_info.type is InvalidCastMember
        assert (
            str(exc_info.value)
            == "Type must be a valid CastMemberType: ACTOR or DIRECTOR"
        )
        mock_repository.update.assert_not_called()  # type: ignore
