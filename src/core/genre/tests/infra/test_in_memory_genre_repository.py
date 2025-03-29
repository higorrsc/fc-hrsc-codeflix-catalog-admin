import uuid

from src.core.genre.domain.genre import Genre
from src.core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository


class TestSave:
    """
    Test that a genre can be saved to the in-memory repository.
    """

    def test_can_save_genre(self):
        """
        Test that a genre can be saved to the in-memory repository.

        This test verifies that the `save` method of the `InMemoryGenreRepository`
        successfully adds a `Genre` instance to its internal genre list.
        """

        repository = InMemoryGenreRepository()
        genre = Genre(name="Action", categories=set())
        repository.save(genre)
        assert genre in repository.genres


class TestGetById:
    """
    Test that a genre can be retrieved from the in-memory repository by its ID.
    """

    def test_can_get_genre_by_id(self):
        """
        Test that a genre can be retrieved from the in-memory repository by its ID.

        This test verifies that the `get_by_id` method of the `InMemoryGenreRepository`
        returns the correct `Genre` instance based on its ID.
        """

        repository = InMemoryGenreRepository()
        genre = Genre(name="Action", categories=set())
        repository.save(genre)
        assert repository.get_by_id(genre.id) == genre

    def test_can_get_nonexistent_genre_by_id(self):
        """
        Test that a non-existent genre cannot be retrieved from the in-memory repository.

        This test verifies that the `get_by_id` method of the `InMemoryGenreRepository`
        returns `None` for a genre ID that does not exist in the repository.
        """

        repository = InMemoryGenreRepository()
        assert repository.get_by_id(uuid.uuid4()) is None


class TestDelete:
    """
    Test that a genre can be deleted from the in-memory repository.
    """

    def test_can_delete_genre(self):
        """
        Test that a genre can be deleted from the in-memory repository.

        This test verifies that the `delete` method of the `InMemoryGenreRepository`
        successfully removes a `Genre` instance from its internal genre list.
        """

        repository = InMemoryGenreRepository()
        genre = Genre(name="Action", categories=set())
        repository.save(genre)
        assert genre in repository.genres
        repository.delete(genre.id)
        assert genre not in repository.genres


class TestUpdate:
    """
    Test that a genre can be updated in the in-memory repository.
    """

    def test_can_update_genre(self):
        """
        Test that a genre can be updated in the in-memory repository.

        This test verifies that the `update` method of the `InMemoryGenreRepository`
        successfully updates a `Genre` instance in its internal genre list.
        """

        repository = InMemoryGenreRepository()
        genre = Genre(name="Action", categories=set())
        repository.save(genre)
        assert genre in repository.genres
        genre.name = "Drama"
        repository.update(genre)
        assert genre in repository.genres


class TestList:
    """
    Test that a list of genres can be retrieved from the in-memory repository.
    """

    def test_can_list_genres(self):
        """
        Test that a list of genres can be retrieved from the in-memory repository.

        This test verifies that the `list` method of the `InMemoryGenreRepository`
        returns a list of `Genre` instances from its internal genre list.
        """

        repository = InMemoryGenreRepository()
        genre = Genre(name="Action", categories=set())
        genre2 = Genre(name="Drama", categories=set())
        repository.save(genre)
        repository.save(genre2)
        assert repository.list() == [genre, genre2]
