import uuid

import pytest

from src.core.cast_member.application.exceptions import (
    CastMemberNotFound,
    InvalidCastMember,
)
from src.core.cast_member.application.use_cases.update_cast_member import (
    UpdateCastMember,
)
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.infra.in_memory_cast_member_repository import (
    InMemoryCastMemberRepository,
)


class TestUpdateCastMember:
    """
    A class for testing the UpdateCastMember use case.
    """

    def test_when_cast_member_is_found(self):
        """
        When calling update_cast_member() with a valid cast member ID,
        it updates the cast member in the repository.
        """

        cast_member = CastMember(
            id=uuid.uuid4(),
            name="Robert Downey Jr.",
            type=CastMemberType.ACTOR,
        )
        repository = InMemoryCastMemberRepository(cast_members=[cast_member])

        use_case = UpdateCastMember(repository)
        use_case.execute(
            UpdateCastMember.Input(
                id=cast_member.id,
                name="John Doe",
                type=CastMemberType.DIRECTOR,
            )
        )

        updated_cast_member = repository.get_by_id(cast_member.id)

        assert updated_cast_member.name == "John Doe"  # type: ignore
        assert updated_cast_member.type == CastMemberType.DIRECTOR  # type: ignore

    def test_when_cast_member_is_not_found(self):
        """
        When calling update_cast_member() with a non-existent cast member ID,
        it raises a CastMemberNotFound exception.
        """

        use_case = UpdateCastMember(InMemoryCastMemberRepository())
        with pytest.raises(CastMemberNotFound):
            use_case.execute(
                UpdateCastMember.Input(
                    id=uuid.uuid4(),
                    name="John Doe",
                    type=CastMemberType.DIRECTOR,
                )
            )

    def test_when_cast_member_name_is_invalid(self):
        """
        When calling update_cast_member() with a cast member name that is too long,
        it raises an InvalidCastMember exception with the message
        "Name must have less then 256 characters".
        """

        cast_member = CastMember(
            id=uuid.uuid4(),
            name="Robert Downey Jr.",
            type=CastMemberType.ACTOR,
        )
        repository = InMemoryCastMemberRepository(cast_members=[cast_member])

        use_case = UpdateCastMember(repository)
        with pytest.raises(InvalidCastMember) as exc_info:
            use_case.execute(
                UpdateCastMember.Input(
                    id=cast_member.id,
                    name="a" * 256,
                    type=CastMemberType.DIRECTOR,
                )
            )

        assert exc_info.type is InvalidCastMember
        assert str(exc_info.value) == "Name must have less then 256 characters"

    def test_when_cast_member_name_is_empty(self):
        """
        When calling update_cast_member() with a cast member name that is empty,
        it raises an InvalidCastMember exception with the message "Name cannot be empty".
        """

        cast_member = CastMember(
            id=uuid.uuid4(),
            name="Robert Downey Jr.",
            type=CastMemberType.ACTOR,
        )
        repository = InMemoryCastMemberRepository(cast_members=[cast_member])

        use_case = UpdateCastMember(repository)
        with pytest.raises(InvalidCastMember) as exc_info:
            use_case.execute(
                UpdateCastMember.Input(
                    id=cast_member.id,
                    name="",
                    type=CastMemberType.DIRECTOR,
                )
            )

        assert exc_info.type is InvalidCastMember
        assert str(exc_info.value) == "Name cannot be empty"

    def test_when_cast_member_type_is_invalid(self):
        """
        When calling update_cast_member() with a cast member type that is invalid,
        it raises an InvalidCastMember exception with the message
        "Type must be a valid CastMemberType: ACTOR or DIRECTOR".
        """

        cast_member = CastMember(
            id=uuid.uuid4(),
            name="Robert Downey Jr.",
            type=CastMemberType.ACTOR,
        )
        repository = InMemoryCastMemberRepository(cast_members=[cast_member])

        use_case = UpdateCastMember(repository)
        with pytest.raises(InvalidCastMember) as exc_info:
            use_case.execute(
                UpdateCastMember.Input(
                    id=cast_member.id,
                    name="John Doe",
                    type="",  # type: ignore
                )
            )

        assert exc_info.type is InvalidCastMember
        assert (
            str(exc_info.value)
            == "Type must be a valid CastMemberType: ACTOR or DIRECTOR"
        )
