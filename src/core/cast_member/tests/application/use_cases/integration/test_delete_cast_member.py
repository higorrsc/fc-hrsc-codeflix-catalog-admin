import uuid

import pytest

from src.core._shared.application.use_cases.delete import DeleteRequest
from src.core.cast_member.application.exceptions import CastMemberNotFound
from src.core.cast_member.application.use_cases.delete_cast_member import (
    DeleteCastMember,
)
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.infra.in_memory_cast_member_repository import (
    InMemoryCastMemberRepository,
)


class TestDeleteCastMember:
    """
    A class for testing the DeleteCastMember use case.
    """

    def test_delete_cast_member_from_repository(self):
        """
        When calling delete_cast_member() with a valid cast member ID, it deletes the
        cast member from the repository.

        The test verifies that when a valid ID is provided, the DeleteCastMember
        use case successfully deletes the cast member from the repository and calls
        the delete method on the repository once with the correct argument.
        """

        repository = InMemoryCastMemberRepository()
        cast_member = CastMember(name="Robert Downey Jr.", type=CastMemberType.ACTOR)
        repository.save(cast_member)

        assert cast_member in repository.list()
        assert repository.get_by_id(cast_member.id) == cast_member

        use_case = DeleteCastMember(repository)
        use_case.execute(DeleteRequest(id=cast_member.id))

        assert cast_member not in repository.list()
        assert repository.get_by_id(cast_member.id) is None

    def test_cast_member_not_found(self):
        """
        Test that attempting to delete a non-existent cast member raises a
        CastMemberNotFound exception.

        This test sets up a repository with a single cast member and then attempts to delete
        a cast member with a randomly generated ID that does not exist in the repository.
        It verifies that the DeleteCastMember use case raises a CastMemberNotFound exception,
        and ensures that the existing cast member remains in the repository.
        """

        repository = InMemoryCastMemberRepository()
        cast_member = CastMember(name="Robert Downey Jr.", type=CastMemberType.ACTOR)
        repository.save(cast_member)

        use_case = DeleteCastMember(repository)
        with pytest.raises(CastMemberNotFound):
            use_case.execute(DeleteRequest(id=uuid.uuid4()))

        assert cast_member in repository.list()
