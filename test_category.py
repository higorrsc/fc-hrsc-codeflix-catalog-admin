import uuid

import pytest

from category import Category


class TestCategory:
    """
    Test the Category class.
    """

    def test_name_is_required(self):
        """
        When creating a Category, name is a required argument.

        A TypeError is raised if no name is provided.
        """
        with pytest.raises(
            TypeError,
            match="missing 1 required positional argument",
        ):
            Category()

    def test_name_must_have_less_then_255_characters(self):
        """
        When creating a Category, name must have less then 256 characters.

        A ValueError is raised if the name has more then 255 characters.
        """
        with pytest.raises(
            ValueError,
            match="Name must have less then 256 characters",
        ):
            Category("a" * 256)

    def test_id_is_generated_as_uuid_if_not_provided(self):
        """
        When creating a Category without id, one is generated as a UUID.
        """
        category = Category("Action")
        assert isinstance(category.id, uuid.UUID)

    def test_create_category_with_default_values(self):
        """
        When creating a Category, without description and is_active, they receive
        default values: description is an empty string and is_active is True.
        """
        category = Category("Action")
        assert category.name == "Action"
        assert category.description == ""
        assert category.is_active is True

    def test_category_is_created_as_active_by_default(self):
        """
        When creating a Category, is_active is True by default.
        """
        category = Category("Action")
        assert category.is_active is True

    def test_category_is_created_with_provided_values(self):
        """
        When creating a Category with provided values, all of them are set to
        the object: name, id, description and is_active.
        """
        category_id = uuid.uuid4()
        category = Category(
            "Action",
            category_id,
            "Action description",
            False,
        )
        assert category.name == "Action"
        assert category.id == category_id
        assert category.description == "Action description"
        assert category.is_active is False

    def test_str_representation(self):
        """
        When calling str() on a Category instance, a human-readable string
        representation is returned.
        """
        category = Category("Action")
        assert str(category) == "Category(Action -  (True))"

    def test_repr_representation(self):
        """
        When calling repr() on a Category instance, an unambiguous string
        representation is returned for debugging.
        """
        category_id = uuid.uuid4()
        category = Category("Action", category_id)
        assert repr(category) == f"<Category Action ({category_id})>"
