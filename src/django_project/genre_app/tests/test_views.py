import pytest
from rest_framework.status import HTTP_200_OK
from rest_framework.test import APIClient

from src.core.category.domain.category import Category
from src.core.genre.domain.genre import Genre
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.genre_app.repository import DjangoORMGenreRepository


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
def category_repository(
    movie_category: Category,
    documentary_category: Category,
) -> DjangoORMCategoryRepository:
    """
    Fixture for a DjangoORMCategoryRepository instance with the movie and documentary
    categories.

    This fixture is used to provide a CategoryRepository that contains the movie and
    documentary categories, which can then be used in tests to verify that the
    get_categories_list use case returns the correct categories.

    Returns:
        DjangoORMCategoryRepository: A CategoryRepository containing the movie and
        documentary categories.
    """
    repository = DjangoORMCategoryRepository()
    repository.save(movie_category)
    repository.save(documentary_category)
    return repository


@pytest.fixture
def romance_genre(
    movie_category: Category,
    documentary_category: Category,
) -> Genre:
    """
    Fixture for a Genre instance representing Romance movies.

    Returns:
        Genre: A Genre object with name "Romance" and the movie and documentary categories.
    """
    return Genre(
        name="Romance",
        categories={
            movie_category.id,
            documentary_category.id,
        },
    )


@pytest.fixture
def drama_genre() -> Genre:
    """
    Fixture for a Genre instance representing Drama movies.

    Returns:
        Genre: A Genre object with name "Drama".
    """
    return Genre(
        name="Drama",
        categories=set(),
    )


@pytest.fixture
def genre_repository() -> DjangoORMGenreRepository:
    """
    Fixture for a DjangoORMGenreRepository instance.

    Returns:
        DjangoORMGenreRepository: A GenreRepository object.
    """

    return DjangoORMGenreRepository()


@pytest.mark.django_db
class TestListAPI:
    """
    Class for testing the ListGenreAPI view.
    """

    def test_list_genres_and_categories(
        self,
        romance_genre: Genre,
        drama_genre: Genre,
        genre_repository: DjangoORMGenreRepository,
        documentary_category: Category,
        movie_category: Category,
        category_repository: DjangoORMCategoryRepository,
    ):
        """
        Tests the ListGenreAPI view.

        Given a DjangoORMGenreRepository with two genres (Romance and Drama) and a
        DjangoORMCategoryRepository with two categories (Movie and Documentary), when
        the ListGenreAPI view is called with a GET request to "/api/genres/", the
        expected output is a JSON response containing a list of two dictionaries
        representing the two genres.

        Each dictionary has the following keys:
        - id: the UUID of the genre
        - name: the name of the genre
        - is_active: whether the genre is active or not
        - categories: a list of the UUIDs of the categories associated with the genre

        The test verifies that the genres are correctly serialized and the response
        contains the expected data.

        """
        genre_repository.save(romance_genre)
        genre_repository.save(drama_genre)

        url = "/api/genres/"
        response = APIClient().get(url)

        # TODO: implement order before assert
        # expected_response = {
        #     "data": [
        #         {
        #             "id": str(romance_genre.id),
        #             "name": romance_genre.name,
        #             "is_active": romance_genre.is_active,
        #             "categories": [
        #                 str(movie_category.id),
        #                 str(documentary_category.id),
        #             ],
        #         },
        #         {
        #             "id": str(drama_genre.id),
        #             "name": drama_genre.name,
        #             "is_active": drama_genre.is_active,
        #             "categories": [],
        #         },
        #     ]
        # }
        # assert response.data["data"] == expected_response  # type: ignore

        assert response.status_code == HTTP_200_OK  # type: ignore
        assert response.data["data"]  # type: ignore
        assert response.data["data"][0]["id"] == str(romance_genre.id)  # type: ignore
        assert response.data["data"][0]["name"] == "Romance"  # type: ignore
        assert response.data["data"][0]["is_active"] is True  # type: ignore
        assert set(response.data["data"][0]["categories"]) == {  # type: ignore
            str(documentary_category.id),
            str(movie_category.id),
        }
        assert response.data["data"][1]["id"] == str(drama_genre.id)  # type: ignore
        assert response.data["data"][1]["name"] == "Drama"  # type: ignore
        assert response.data["data"][1]["is_active"] is True  # type: ignore
        assert response.data["data"][1]["categories"] == []  # type: ignore
