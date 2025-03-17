import uuid

import pytest

from src.core.cast_member.domain.cast_member import CastMember, CastMemberType


class TestCastMember:
    """
    Test the CastMember class
    """

    def test_name_is_required(self):
        """
        When creating a CastMember, name is a required argument.

        A TypeError is raised if no name is provided.
        """

        with pytest.raises(
            ValueError,
            match="Name cannot be empty",
        ):
            CastMember(
                name="",
                type=CastMemberType.ACTOR,
            )

    def test_name_is_longer_than_255_characters(self):
        """
        When creating a CastMember, name is a required argument.

        A ValueError is raised if the name is longer than 255 characters.
        """

        with pytest.raises(
            ValueError,
            match="Name must have less then 256 characters",
        ):
            CastMember(
                name="a" * 256,
                type=CastMemberType.ACTOR,
            )

    def test_type_is_required(self):
        """
        When creating a CastMember, type is a required argument.

        A TypeError is raised if no type is provided.
        """

        with pytest.raises(
            ValueError,
            match="Type must be a valid CastMemberType: ACTOR or DIRECTOR",
        ):
            CastMember(
                name="Robert Downey Jr.",
                type=None,  # type: ignore
            )

    def test_id_is_auto_generated(self):
        """
        When creating a CastMember, the id should be auto-generated.
        """

        cast_member = CastMember(
            name="Robert Downey Jr.",
            type=CastMemberType.ACTOR,
        )

        assert isinstance(cast_member.id, uuid.UUID)

    def test_cast_member_is_created(self):
        """
        When creating a CastMember, it should be created successfully.
        """
        cast_member_id = uuid.uuid4()
        cast_member = CastMember(
            name="Robert Downey Jr.",
            type=CastMemberType.ACTOR,
            id=cast_member_id,
        )

        assert cast_member.name == "Robert Downey Jr."
        assert cast_member.type == CastMemberType.ACTOR
        assert cast_member.id == cast_member_id

    def test_str_representation(self):
        """
        When calling str() on a CastMember instance, a human-readable string
        representation is returned.
        """

        cast_member = CastMember("Robert Downey Jr.", CastMemberType.ACTOR)
        assert str(cast_member) == "CastMember(Robert Downey Jr. - ACTOR)"

    def test_repr_representation(self):
        """
        When calling repr() on a CastMember instance, an unambiguous string
        representation is returned.
        """

        cast_member_id = uuid.uuid4()
        cast_member = CastMember(
            name="Robert Downey Jr.",
            type=CastMemberType.ACTOR,
            id=cast_member_id,
        )

        assert repr(cast_member) == f"<CastMember Robert Downey Jr. ({cast_member_id})>"


class TestUpdateCastMember:
    """
    Test the CastMember class
    """

    def test_not_update_when_name_is_empty(self):
        """
        When updating a CastMember's name with an empty string, a ValueError should be raised.

        This test ensures that the `update_cast_member` method raises a ValueError
        when the name provided is empty.
        """

        cast_member = CastMember(
            name="Clint Eastwood",
            type=CastMemberType.ACTOR,
        )

        with pytest.raises(
            ValueError,
            match="Name cannot be empty",
        ):
            cast_member.update_cast_member(
                name="",
                type=CastMemberType.DIRECTOR,
            )

    def test_not_update_when_name_is_longer_than_255_characters(self):
        """
        When updating a CastMember with a name that is longer than 255 characters,
        a ValueError should be raised.
        """

        cast_member = CastMember(
            name="Clint Eastwood",
            type=CastMemberType.ACTOR,
        )

        with pytest.raises(
            ValueError,
            match="Name must have less then 256 characters",
        ):
            cast_member.update_cast_member(
                name="a" * 256,
                type=CastMemberType.DIRECTOR,
            )

    def test_not_update_when_type_is_invalid(self):
        """
        When trying to update a CastMember with an invalid type, a ValueError is raised.

        This test ensures that the `update_cast_member` method raises a ValueError
        when the type provided is not a valid CastMemberType.
        """

        cast_member = CastMember(
            name="Clint Eastwood",
            type=CastMemberType.ACTOR,
        )

        with pytest.raises(
            ValueError,
            match="Type must be a valid CastMemberType: ACTOR or DIRECTOR",
        ):
            cast_member.update_cast_member(
                name="Clint Eastwood",
                type="invalid",  # type: ignore
            )

    def test_update_cast_member_name(self):
        """
        When updating a CastMember's name, the CastMember should reflect the new name.

        Given a CastMember with a name,
        when we call update_cast_member with a new name,
        the CastMember should have the new name.
        """

        cast_member = CastMember(
            name="Clint Eastwood",
            type=CastMemberType.ACTOR,
        )

        cast_member.update_cast_member(
            name="Robert Downey Jr.",
            type=CastMemberType.ACTOR,
        )

        assert cast_member.name == "Robert Downey Jr."
        assert cast_member.type == CastMemberType.ACTOR

    def test_update_cast_member_type(self):
        """
        When updating a CastMember's type, the CastMember should reflect the new type.

        This test ensures that the `update_cast_member` method correctly updates the
        type of a CastMember while keeping the name unchanged.
        """

        cast_member = CastMember(
            name="Clint Eastwood",
            type=CastMemberType.ACTOR,
        )

        cast_member.update_cast_member(
            name="Clint Eastwood",
            type=CastMemberType.DIRECTOR,
        )

        assert cast_member.name == "Clint Eastwood"
        assert cast_member.type == CastMemberType.DIRECTOR


class TestEquality:
    """
    Test the CastMember class
    """

    def test_cast_member_equality(self):
        """
        When comparing two CastMember instances, they should be equal if their
        ids, names and types are the same.
        """

        common_id = uuid.uuid4()
        cast_member1 = CastMember("Clint Eastwood", CastMemberType.ACTOR, common_id)
        cast_member2 = CastMember("Clint Eastwood", CastMemberType.ACTOR, common_id)

        assert cast_member1 == cast_member2

    def test_cast_member_inequality(self):
        """
        When comparing two CastMember instances, they should not be equal if their
        ids, names or types are different.
        """

        common_id = uuid.uuid4()
        cast_member1 = CastMember("Clint Eastwood", CastMemberType.ACTOR, common_id)
        cast_member2 = CastMember("Clint Eastwood", CastMemberType.DIRECTOR, common_id)

        assert cast_member1 != cast_member2

    def test_cast_member_inequality_with_different_classes(self):
        """
        When comparing a CastMember instance with a different class, they should not be equal.
        """

        class Dummy:
            """
            Dummy class to test equality.
            """

        common_id = uuid.uuid4()
        cast_member1 = CastMember("Clint Eastwood", CastMemberType.ACTOR, common_id)
        dummy = Dummy()
        dummy.id = common_id  # type: ignore

        assert cast_member1 != dummy
