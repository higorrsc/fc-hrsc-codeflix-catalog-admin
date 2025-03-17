import pytest

from src.core.cast_member.application.exceptions import InvalidCastMember
from src.core.cast_member.application.use_cases.create_cast_member import (
    CreateCastMember,
)
from src.core.cast_member.domain.cast_member import CastMemberType
from src.core.cast_member.infra.in_memory_cast_member_repository import (
    InMemoryCastMemberRepository,
)


class TestCreateCastMember:
    """
    Test suite for the CreateCastMember use case.
    """

    def test_create_cast_member_with_valid_data(self):
        """
        When creating a cast member with valid data, it should be created successfully.

        This test verifies that when valid data is provided, the CreateCastMember
        use case successfully creates a new cast member, assigns a non-null ID,
        returns an instance of CreateCastMember.Output, and saves the cast member
        in the repository.
        """

        repository = InMemoryCastMemberRepository()
        use_case = CreateCastMember(repository)
        output = use_case.execute(
            CreateCastMember.Input(
                name="John Doe",
                type=CastMemberType.ACTOR,
            )
        )

        assert output.id is not None
        assert isinstance(output, CreateCastMember.Output)
        assert len(repository.cast_members) == 1

    def test_create_cast_member_with_invalid_name(self):
        """
        Test that creating a cast member with an empty name raises an InvalidCastMember
        exception with the message "Name cannot be empty".

        This test verifies that when an empty string is provided as the name, the
        CreateCastMember use case raises an InvalidCastMember exception with the
        correct message.
        """

        use_case = CreateCastMember(InMemoryCastMemberRepository())
        with pytest.raises(InvalidCastMember, match="Name cannot be empty") as exc_info:
            use_case.execute(
                CreateCastMember.Input(
                    name="",
                    type=CastMemberType.ACTOR,
                )
            )

        assert exc_info.type is InvalidCastMember
        assert str(exc_info.value) == "Name cannot be empty"

    def test_create_cast_member_with_invalid_type(self):
        """
        Test that creating a cast member with an invalid type raises an InvalidCastMember
        exception with the message "Type must be a valid CastMemberType: ACTOR or DIRECTOR".

        This test verifies that when an invalid type is provided, the CreateCastMember
        use case raises an InvalidCastMember exception with the correct message.
        """

        use_case = CreateCastMember(InMemoryCastMemberRepository())
        with pytest.raises(
            InvalidCastMember,
            match="Type must be a valid CastMemberType: ACTOR or DIRECTOR",
        ) as exc_info:
            use_case.execute(
                CreateCastMember.Input(
                    name="John Doe",
                    type="",  # type: ignore
                )
            )

        assert exc_info.type is InvalidCastMember
        assert (
            str(exc_info.value)
            == "Type must be a valid CastMemberType: ACTOR or DIRECTOR"
        )
