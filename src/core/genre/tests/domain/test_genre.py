import uuid

import pytest

from src.core.genre.domain.genre import Genre


class TestGenre:
    """
    Test the Genre class.
    """

    def test_name_is_required(self):
        """
        When creating a Genre, name is a required argument.

        A TypeError is raised if no name is provided.
        """

        with pytest.raises(
            TypeError,
            match="missing 1 required positional argument",
        ):
            Genre()  # type: ignore

    def test_cannot_create_genre_with_empty_name(self):
        """
        When creating a Genre with an empty name, a ValueError is raised.
        """

        with pytest.raises(
            ValueError,
            match="Name cannot be empty",
        ):
            Genre("")

    def test_name_must_have_less_then_255_characters(self):
        """
        When creating a Genre, name must have less then 256 characters.

        A ValueError is raised if the name has more then 255 characters.
        """

        with pytest.raises(
            ValueError,
            match="Name must have less then 256 characters",
        ):
            Genre("a" * 256)

    def test_create_genre_with_default_values(self):
        """
        When creating a Genre without providing id, description,
        is_active, and categories, they receive default values:
        id is a UUID, description is an empty string, is_active is True,
        and categories is an empty set.
        """

        genre = Genre("Romance")
        assert genre.name == "Romance"
        assert genre.is_active is True
        assert isinstance(genre.id, uuid.UUID)
        assert genre.categories == set()

    def test_genre_is_created_with_provided_values(self):
        """
        When creating a Genre with provided values, all of them are set to
        the object: name, id, is_active and categories.
        """

        genre_id = uuid.uuid4()
        categories_ids = {uuid.uuid4(), uuid.uuid4()}
        genre = Genre(
            "Romance",
            genre_id,
            False,
            categories_ids,
        )
        assert genre.name == "Romance"
        assert genre.id == genre_id
        assert genre.is_active is False
        assert genre.categories == categories_ids

    def test_str_representation(self):
        """
        When calling str() on a Genre instance, a human-readable string
        representation is returned.
        """

        genre = Genre("Romance")
        assert str(genre) == "Genre(Romance (True))"

    def test_repr_representation(self):
        """
        When calling repr() on a Genre instance, an unambiguous string
        representation is returned for debugging.
        """

        genre_id = uuid.uuid4()
        genre = Genre("Romance", genre_id)
        assert repr(genre) == f"<Genre Romance ({genre_id})>"


class TestChangeGenreName:
    """
    Test the change_name function.
    """

    def test_update_genre_with_name_and_description(self):
        """
        When calling change_name() on a Genre instance, passing the name and description,
        the genre's name and description are updated.
        """

        genre = Genre(name="Romance")
        genre.change_name("Adventure")
        assert genre.name == "Adventure"

    def test_update_genre_with_invalid_name_raises_exception(self):
        """
        When calling change_name() with a name longer than 255 characters,
        a ValueError is raised.
        """

        genre = Genre(name="Romance")
        with pytest.raises(
            ValueError,
            match="Name must have less then 256 characters",
        ):
            genre.change_name("a" * 256)

    def test_cannot_update_genre_with_empty_name(self):
        """
        When calling change_name() with an empty name, a ValueError is raised.
        """

        genre = Genre(name="Romance")
        with pytest.raises(
            ValueError,
            match="Name cannot be empty",
        ):
            genre.change_name("")


class TestActivateGenre:
    """
    Test the activate function.
    """

    def test_activate_inactive_genre(self):
        """
        When calling activate() on a Genre instance, the genre is activated.
        """

        genre = Genre(
            name="Romance",
            is_active=False,
        )
        genre.activate()
        assert genre.is_active is True

    def test_activate_active_genre(self):
        """
        When calling activate() on a Genre instance, the genre is not activated.
        """

        genre = Genre(
            name="Romance",
            is_active=True,
        )
        genre.activate()
        assert genre.is_active is True


class TestDeactivateGenre:
    """
    Test the deactivate function.
    """

    def test_deactivate_active_genre(self):
        """
        When calling deactivate() on a Genre instance, the genre is deactivated.
        """

        genre = Genre(
            name="Romance",
            is_active=True,
        )
        genre.deactivate()
        assert genre.is_active is False

    def test_deactivate_inactive_genre(self):
        """
        When calling deactivate() on a Genre instance, the genre is not deactivated.
        """

        genre = Genre(
            name="Romance",
            is_active=False,
        )
        genre.deactivate()
        assert genre.is_active is False


class TestEquality:
    """
    Test the __eq__ function.
    """

    def test_genre_equality(self):
        """
        When creating two Genre instances with the same name and id, they are considered equal.
        """

        common_id = uuid.uuid4()
        genre1 = Genre("Romance", common_id)
        genre2 = Genre("Romance", common_id)
        assert genre1 == genre2

    def test_equality_different_classes(self):
        """
        When comparing a Genre instance with an instance of a different class
        having the same id, they are not considered equal.
        """

        class Dummy:
            """
            Dummy class to test equality.
            """

        common_id = uuid.uuid4()
        genre = Genre("Romance", common_id)
        dummy = Dummy()
        dummy.id = common_id  # type: ignore
        assert genre != dummy


class TestAddCategory:
    """
    Test the add_category function.
    """

    def test_add_category(self):
        """
        When calling add_category() on a Genre instance, the category is added.
        """

        genre = Genre("Romance")
        category_id = uuid.uuid4()
        assert category_id not in genre.categories

        genre.add_category(category_id)
        assert category_id in genre.categories

    def test_can_add_multiple_categories(self):
        """
        When calling add_category() on a Genre instance, multiple categories can be added.
        """

        genre = Genre("Romance")
        category_id1 = uuid.uuid4()
        category_id2 = uuid.uuid4()

        genre.add_category(category_id1)
        genre.add_category(category_id2)

        assert len(genre.categories) == 2
        assert category_id1 in genre.categories
        assert category_id2 in genre.categories
        assert genre.categories == {
            category_id1,
            category_id2,
        }


class TestRemoveCategory:
    """
    Test the remove_category function.
    """

    def test_remove_category(self):
        """
        When calling remove_category() on a Genre instance, the category is removed.
        """

        genre = Genre("Romance")
        category_id = uuid.uuid4()
        genre.add_category(category_id)
        assert category_id in genre.categories

        genre.remove_category(category_id)
        assert category_id not in genre.categories
        assert genre.categories == set()
