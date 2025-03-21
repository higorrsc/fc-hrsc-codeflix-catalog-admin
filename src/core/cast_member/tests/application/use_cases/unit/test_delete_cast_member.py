import uuid
from unittest.mock import create_autospec

import pytest

from src.core.cast_member.application.exceptions import CastMemberNotFound
from src.core.cast_member.application.use_cases.delete_cast_member import (
    DeleteCastMember,
)
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


class TestDeleteCastMember:
    """
    A class for testing the DeleteCastMember use case.
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
    def mock_repository(self, actor: CastMember):
        """
        A fixture that returns a mock repository containing the actor CastMember.

        This fixture returns a mock repository where the get_by_id method returns the
        actor CastMember. This is used in tests to simulate a scenario where the
        repository contains a known cast member, allowing for testing of behavior
        when a cast member is found.
        """

        repository = create_autospec(CastMemberRepository)
        repository.get_by_id.return_value = actor
        return repository

    @pytest.fixture
    def mock_empty_repository(self):
        """
        A fixture that returns a repository where no CastMembers exist.

        This fixture is used in tests to simulate a scenario where
        the repository does not contain any cast members, allowing
        for testing of behavior when a cast member is not found.
        """

        repository = create_autospec(CastMemberRepository)
        repository.get_by_id.return_value = None
        return repository

    def test_delete_cast_member_from_repository(
        self,
        actor: CastMember,
        mock_repository: CastMemberRepository,
    ):
        """
        When calling delete_cast_member() with a valid cast member ID, it deletes the
        cast member from the repository.

        The test verifies that when a valid ID is provided, the DeleteCastMember
        use case successfully deletes the cast member from the repository and calls
        the delete method on the repository once with the correct argument.
        """

        use_case = DeleteCastMember(mock_repository)
        use_case.execute(DeleteCastMember.Input(id=actor.id))

        mock_repository.delete.assert_called_once_with(actor.id)  # type: ignore

    def test_cast_member_not_found(
        self,
        mock_empty_repository: CastMemberRepository,
    ):
        """
        When calling delete_cast_member() with a non-existent cast member ID, it raises a
        CastMemberNotFound exception.

        This test verifies that the `delete_cast_member` use case raises a
        CastMemberNotFound exception when the cast member is not found in the repository.
        """

        use_case = DeleteCastMember(mock_empty_repository)
        with pytest.raises(CastMemberNotFound):
            use_case.execute(DeleteCastMember.Input(id=uuid.uuid4()))

        mock_empty_repository.delete.assert_not_called()  # type: ignore
