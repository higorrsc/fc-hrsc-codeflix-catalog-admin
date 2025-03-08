from src.core.genre.application.use_cases.delete_genre import DeleteGenre
from src.core.genre.domain.genre import Genre
from src.core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository


class TestDeleteGenre:
    """
    Test suite for the DeleteGenre use case.
    """

    def test_delete_genre_from_repository(self):
        """
        When calling delete_genre() with a valid genre ID, it deletes the genre
        from the repository.

        This test verifies that the `delete_genre` use case successfully deletes
        a genre by its ID from the repository.
        """

        genre = Genre(name="Action")
        repository = InMemoryGenreRepository()
        repository.save(genre)
        assert repository.get_by_id(genre.id) == genre

        use_case = DeleteGenre(repository=repository)
        use_case.execute(input=DeleteGenre.Input(id=genre.id))

        assert repository.get_by_id(genre.id) is None
        assert len(repository.genres) == 0
