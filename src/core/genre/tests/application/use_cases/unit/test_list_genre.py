from unittest.mock import create_autospec

import pytest

from src.config import DEFAULT_PAGE_SIZE
from src.core._shared.application.use_cases.list import (
    ListRequest,
    ListResponse,
    ListResponseMeta,
)
from src.core.category.domain.category import Category
from src.core.genre.application.use_cases.list_genre import ListGenre
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository


@pytest.fixture
def movie_category() -> Category:
    """
    Fixture for a Category instance representing movies.

    Returns:
        Category: A Category object with name "Movie" and description "Movies category".
    """

    return Category(
        name="Movie",
        description="Movies category",
    )


@pytest.fixture
def documentary_category() -> Category:
    """
    Fixture for a Category instance representing documentaries.

    Returns:
        Category: A Category object with name "Documentary" and description "Documentary category".
    """

    return Category(
        name="Documentary",
        description="Documentary category",
    )


@pytest.fixture
def horror_genre(movie_category: Category) -> Genre:
    """
    Fixture for a Genre instance representing Horror movies.

    Returns:
        Genre: A Genre object with name "Horror" and the movie category.
    """
    return Genre(
        name="Horror",
        categories={
            movie_category.id,
        },
    )


@pytest.fixture
def noir_genre(movie_category: Category, documentary_category: Category) -> Genre:
    """
    Fixture for a Genre instance representing Noir movies.

    Returns:
        Genre: A Genre object with name "Noir" and the movie and documentary categories.
    """
    return Genre(
        name="Noir",
        categories={
            movie_category.id,
            documentary_category.id,
        },
    )


@pytest.fixture
def mock_genre_repository(horror_genre: Genre, noir_genre: Genre) -> GenreRepository:
    """
    Fixture for a mock GenreRepository instance.

    Returns:
        GenreRepository: A mock GenreRepository object.
    """

    repository = create_autospec(GenreRepository)
    repository.list.return_value = [horror_genre, noir_genre]
    return repository


@pytest.fixture
def mock_empty_genre_repository() -> GenreRepository:
    """
    Fixture for a mock GenreRepository instance.

    Returns:
        GenreRepository: A mock GenreRepository object.
    """

    repository = create_autospec(GenreRepository)
    repository.list.return_value = []
    return repository


class TestListGenre:
    """
    Test the ListGenre class.
    """

    def test_list_genres_with_associated_categories(
        self,
        mock_genre_repository: GenreRepository,
        horror_genre: Genre,
        noir_genre: Genre,
    ):
        """
        When calling list_genres() with a GenreRepository and CategoryRepository,
        it returns a list of GenreOutput objects with associated categories.

        Args:
            mock_genre_repository (GenreRepository): A mock GenreRepository object.

        Returns:
            ListGenre.Output: A ListGenre.Output object containing a list of
            GenreOutput objects with associated categories.
        """

        use_case = ListGenre(repository=mock_genre_repository)
        output: ListResponse = use_case.execute(ListRequest(order_by="name"))

        assert output == {
            "data": [
                horror_genre,
                noir_genre,
            ],
            "meta": ListResponseMeta(
                current_page=1,
                per_page=DEFAULT_PAGE_SIZE,
                total=2,
            ),
        }

    def test_when_no_genre_exists_return_empty_list(
        self,
        mock_empty_genre_repository: GenreRepository,
    ):
        """
        When calling list_genres() with an empty GenreRepository, it returns an empty list.

        Args:
            mock_empty_genre_repository (GenreRepository): A mock GenreRepository object.

        Returns:
            ListGenre.Output: A ListGenre.Output object containing an empty list.
        """

        use_case = ListGenre(repository=mock_empty_genre_repository)
        output: ListResponse = use_case.execute(ListRequest())
        expected_data = {
            "data": [],
            "meta": ListResponseMeta(
                current_page=1,
                per_page=DEFAULT_PAGE_SIZE,
                total=0,
            ),
        }

        assert output == expected_data
