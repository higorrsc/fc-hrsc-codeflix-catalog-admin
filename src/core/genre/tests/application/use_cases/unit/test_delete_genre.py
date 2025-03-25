import uuid
from unittest.mock import create_autospec

import pytest

from src.core._shared.application.use_cases.delete import DeleteRequest
from src.core.genre.application.exceptions import GenreNotFound
from src.core.genre.application.use_cases.delete_genre import DeleteGenre
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository


@pytest.fixture
def mock_genre_repository() -> GenreRepository:
    """
    Fixture for a mock GenreRepository instance.

    Returns:
        GenreRepository: A mock GenreRepository object.
    """

    return create_autospec(GenreRepository)


class TestDeleteGenre:
    """
    Test suite for the DeleteGenre use case.
    """

    def test_delete_genre_from_repository(
        self,
        mock_genre_repository: GenreRepository,
    ):
        """
        When calling delete_genre() with a valid genre ID, it deletes the genre
        from the repository.

        This test verifies that the `delete_genre` use case successfully deletes
        a genre by its ID from the repository.
        """

        genre = Genre(name="Romance")
        mock_genre_repository.get_by_id.return_value = genre  # type: ignore

        use_case = DeleteGenre(repository=mock_genre_repository)
        use_case.execute(request=DeleteRequest(id=genre.id))  # type: ignore

        mock_genre_repository.delete.assert_called_once_with(genre_id=genre.id)  # type: ignore

    def test_when_genre_not_found_raises_exception(
        self,
        mock_genre_repository: GenreRepository,
    ):
        """
        When calling delete_genre() with a non-existent genre ID, it raises a
        GenreNotFound exception.

        This test verifies that the `delete_genre` use case raises a
        GenreNotFound exception when the genre is not found in the repository.
        """

        mock_genre_repository.get_by_id.return_value = None  # type: ignore

        use_case = DeleteGenre(repository=mock_genre_repository)

        with pytest.raises(GenreNotFound, match="Genre with .* not found"):
            use_case.execute(request=DeleteRequest(id=uuid.uuid4()))

        mock_genre_repository.delete.assert_not_called()  # type: ignore
