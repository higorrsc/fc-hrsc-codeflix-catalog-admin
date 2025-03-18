import uuid

import pytest

from src.core.category.domain.category import Category


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
            Category()  # pylint: disable=no-value-for-parameter

    def test_cannot_create_category_with_empty_name(self):
        """
        When creating a Category with an empty name, a ValueError is raised.
        """
        with pytest.raises(
            ValueError,
            match="Name cannot be empty",
        ):
            Category("")

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

    def test_description_must_have_less_then_1024_characters(self):
        """
        When creating a Category, description must have less then 1024 characters.

        A ValueError is raised if the description has more then 1024 characters.
        """

        with pytest.raises(
            ValueError,
            match="Description must have less then 1024 characters",
        ):
            Category("Action", description="a" * 1025)

    def test_name_and_description_lengths(self):
        """
        When creating a Category, name and description must have less then 256 characters.
        """

        with pytest.raises(
            ValueError,
            match="^Name must have less then 256 characters,Description must have less then 1024 characters$",
        ):
            Category(name="a" * 256, description="a" * 1025)

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
            id=category_id,
            name="Action",
            description="Action description",
            is_active=False,
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
        category = Category(
            id=category_id,
            name="Action",
        )
        assert repr(category) == f"<Category Action ({category_id})>"


class TestUpdateCategory:
    """
    Test the update_category function.
    """

    def test_update_category_with_name_and_description(self):
        """
        When calling update_category() on a Category instance, passing the name and description,
        the category's name and description are updated.
        """

        category = Category(
            name="Action",
            description="Action movies",
        )
        category.update_category(
            name="Adventure",
            description="Adventure movies",
        )
        assert category.name == "Adventure"
        assert category.description == "Adventure movies"

    def test_update_category_with_invalid_name_raises_exception(self):
        """
        When calling update_category() with a name longer than 255 characters,
        a ValueError is raised.
        """

        category = Category(name="Action", description="Action movies")
        with pytest.raises(
            ValueError,
            match="Name must have less then 256 characters",
        ):
            category.update_category("a" * 256, "Adventure movies")

    def test_cannot_update_category_with_empty_name(self):
        """
        When calling update_category() with an empty name, a ValueError is raised.
        """

        category = Category(name="Action")
        with pytest.raises(
            ValueError,
            match="Name cannot be empty",
        ):
            category.update_category("", "Adventure movies")


class TestActivateCategory:
    """
    Test the activate function.
    """

    def test_activate_inactive_category(self):
        """
        When calling activate() on a Category instance, the category is activated.
        """

        category = Category(
            name="Action",
            description="Action movies",
            is_active=False,
        )
        category.activate()
        assert category.is_active is True

    def test_activate_active_category(self):
        """
        When calling activate() on a Category instance, the category is not activated.
        """

        category = Category(
            name="Action",
            description="Action movies",
            is_active=True,
        )
        category.activate()
        assert category.is_active is True


class TestDeactivateCategory:
    """
    Test the deactivate function.
    """

    def test_deactivate_active_category(self):
        """
        When calling deactivate() on a Category instance, the category is deactivated.
        """

        category = Category(
            name="Action",
            description="Action movies",
            is_active=True,
        )
        category.deactivate()
        assert category.is_active is False

    def test_deactivate_inactive_category(self):
        """
        When calling deactivate() on a Category instance, the category is not deactivated.
        """

        category = Category(
            name="Action",
            description="Action movies",
            is_active=False,
        )
        category.deactivate()
        assert category.is_active is False


class TestEquality:
    """
    Test the __eq__ function.
    """

    def test_category_equality(self):
        """
        When creating two Category instances with the same name and id, they are considered equal.
        """

        common_id = uuid.uuid4()
        category1 = Category(
            id=common_id,
            name="Action",
        )
        category2 = Category(
            id=common_id,
            name="Action",
        )
        assert category1 == category2

    def test_equality_different_classes(self):
        """
        When comparing a Category instance with an instance of a different class
        having the same id, they are not considered equal.
        """

        class Dummy:
            """
            Dummy class to test equality.
            """

        common_id = uuid.uuid4()
        category = Category(
            id=common_id,
            name="Action",
        )
        dummy = Dummy()
        dummy.id = common_id  # type: ignore
        assert category != dummy
