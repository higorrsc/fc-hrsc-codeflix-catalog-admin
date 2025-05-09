import os
import uuid

import pytest
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)
from rest_framework.test import APIClient

from src.config import DEFAULT_PAGE_SIZE
from src.core._shared.infrastructure.auth.jwt_token_generator import JwtTokenGenerator
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


@pytest.fixture(scope="session", autouse=True)
def setup_auth_env():
    fake_auth = JwtTokenGenerator()
    os.environ["AUTH_PUBLIC_KEY"] = (
        fake_auth.public_key_pem.decode()
        .replace("-----BEGIN PUBLIC KEY-----\n", "")
        .replace("\n-----END PUBLIC KEY-----\n", "")
    )
    return fake_auth


@pytest.fixture
def auth_token(setup_auth_env):
    return setup_auth_env.generate_token(
        user_info={
            "username": "admin",
            "email": "admin@example.com",
            "first_name": "Admin",
            "last_name": "User",
            "realm_roles": [
                "offline_access",
                "admin",
                "uma_authorization",
                "default-roles-codeflix",
            ],
            "resource_roles": [
                "manage-account",
                "view-profile",
            ],
        }
    )


@pytest.fixture
def api_client_with_auth(auth_token):
    """
    Fixture for an API client with authentication.

    Returns:
        APIClient: An instance of the APIClient with the provided authentication token.
    """

    return APIClient(
        headers={
            "Authorization": f"Bearer {auth_token}",
        }
    )


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
        api_client_with_auth: APIClient,
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
        response = api_client_with_auth.get(url)

        expected_response = {
            "data": [
                {
                    "id": str(drama_genre.id),
                    "name": drama_genre.name,
                    "is_active": drama_genre.is_active,
                    "categories": [],
                },
                {
                    "id": str(romance_genre.id),
                    "name": romance_genre.name,
                    "is_active": romance_genre.is_active,
                    "categories": [
                        str(movie_category.id),
                        str(documentary_category.id),
                    ],
                },
            ],
            "meta": {
                "current_page": 1,
                "per_page": DEFAULT_PAGE_SIZE,
                "total": 2,
            },
        }

        assert response.status_code == HTTP_200_OK  # type: ignore
        assert response.data, expected_response  # type: ignore


@pytest.mark.django_db
class TestCreateAPI:
    """
    Class for testing the CreateGenreAPI view.
    """

    def test_create_genre_with_associated_categories(
        self,
        movie_category: Category,
        documentary_category: Category,
        category_repository: DjangoORMCategoryRepository,
        genre_repository: DjangoORMGenreRepository,
        api_client_with_auth: APIClient,
    ):
        """
        Test that the API returns 201 when creating a genre with associated categories.

        When the API is called with POST /api/genres/ and the given data is valid,
        it should return a 201 status code and create a new genre in the database
        with the given name and associated categories.

        The expected result is a 201 status code and that the genre is successfully
        created in the database with the correct data.
        """

        url = "/api/genres/"
        data = {
            "name": "Anime",
            "categories": [
                str(movie_category.id),
                str(documentary_category.id),
            ],
        }
        response = api_client_with_auth.post(
            path=url,
            data=data,
            format="json",
        )

        assert response.status_code == HTTP_201_CREATED  # type: ignore
        assert response.data["id"]  # type: ignore

        genre_model = genre_repository.get_by_id(genre_id=response.data["id"])  # type: ignore
        assert genre_model.id == uuid.UUID(response.data["id"])  # type: ignore
        assert genre_model.name == "Anime"  # type: ignore
        assert genre_model.is_active is True  # type: ignore
        assert genre_model == Genre(
            id=genre_model.id,  # type: ignore
            name=genre_model.name,  # type: ignore
            is_active=genre_model.is_active,  # type: ignore
            categories=set(genre_model.categories),  # type: ignore
        )

    def test_create_genre_without_name(
        self,
        api_client_with_auth: APIClient,
    ):
        """
        Test that the API returns 400 when creating a genre without a name.

        When the API is called with POST /api/genres/ and the given data is
        invalid because the name is empty, it should return a 400 status code and
        an error message indicating that the name is required.

        The expected result is a 400 status code and an error message indicating
        that the name is required.
        """

        url = "/api/genres/"
        data = {
            "name": "",
        }
        response = api_client_with_auth.post(
            path=url,
            data=data,
            format="json",
        )

        assert response.status_code == HTTP_400_BAD_REQUEST  # type: ignore
        assert response.data == {"name": ["This field may not be blank."]}  # type: ignore

    def test_create_genre_with_invalid_categories(
        self,
        api_client_with_auth: APIClient,
    ):
        """
        Test that the API returns 400 when creating a genre with invalid category IDs.

        When the API is called with POST /api/genres/ and the given category IDs do not
        exist in the repository, it should return a 400 status code and an error message
        indicating that the categories with the provided IDs were not found.

        The expected result is a 400 status code and an error message indicating that
        the categories with the provided IDs were not found.
        """

        url = "/api/genres/"
        data = {
            "name": "Anime",
            "categories": [uuid.uuid4()],
        }
        response = api_client_with_auth.post(
            path=url,
            data=data,
            format="json",
        )

        assert response.status_code == HTTP_400_BAD_REQUEST  # type: ignore
        assert "Categories with provided IDs not found" in response.data["error"]  # type: ignore


@pytest.mark.django_db
class TestDeleteAPI:
    """
    Class for testing the DeleteGenreAPI view.
    """

    def test_when_genre_not_exists_return_404(
        self,
        api_client_with_auth: APIClient,
    ):
        """
        Test that the API returns 404 when the given genre ID does not exist.

        When the API is called with DELETE /api/genres/<id>/ and the given genre ID
        does not exist, it should return a 404 error with a specific error message.

        The expected result is a 404 status code and an error message indicating
        that the genre was not found.
        """

        url = f"/api/genres/{uuid.uuid4()}/"
        response = api_client_with_auth.delete(url)

        assert response.status_code == HTTP_404_NOT_FOUND  # type: ignore
        assert response.data == {"error": "Genre not found"}  # type: ignore

    def test_when_genre_id_is_invalid_return_400(
        self,
        api_client_with_auth: APIClient,
    ):
        """
        Test that the API returns 400 when the given genre ID is invalid.

        When the API is called with DELETE /api/genres/<id>/ and the given genre ID
        is invalid, it should return a 400 error with a specific error message.

        The expected result is a 400 status code and an error message indicating
        that the genre ID is invalid.
        """

        url = "/api/genres/1234567890/"
        response = api_client_with_auth.delete(url)

        assert response.status_code == HTTP_400_BAD_REQUEST  # type: ignore

    def test_when_genre_is_deleted_return_204(
        self,
        genre_repository: DjangoORMGenreRepository,
        api_client_with_auth: APIClient,
    ):
        """
        Test that the API returns 204 when the given genre ID exists and is deleted.

        When the API is called with DELETE /api/genres/<id>/ and the given genre ID
        exists, it should return a 204 status code and delete the genre from the
        database.

        The expected result is a 204 status code and that the genre is no longer
        found in the database.
        """
        genre = Genre(name="Romance", is_active=False)
        genre_repository.save(genre)

        url = f"/api/genres/{genre.id}/"
        response = api_client_with_auth.delete(url)
        assert response.status_code == HTTP_204_NO_CONTENT  # type: ignore

        genre_model = genre_repository.get_by_id(genre_id=genre.id)
        assert genre_model is None


@pytest.mark.django_db
class TestUpdateAPI:
    """
    Class for testing the UpdateGenreAPI view.
    """

    def test_when_request_data_is_valid_then_update_genre(
        self,
        genre_repository: DjangoORMGenreRepository,
        movie_category: Category,
        category_repository: DjangoORMCategoryRepository,
        api_client_with_auth: APIClient,
    ):
        """
        Test that the API returns 204 when the given genre ID exists and the request
        data is valid.

        When the API is called with PUT /api/genres/<id>/ and the given genre ID exists,
        it should return a 204 status code and update the genre in the database with
        the given data.

        The expected result is a 204 status code and that the genre is successfully
        updated in the database with the correct data.
        """

        genre = Genre(name="Horror", is_active=False)
        genre_repository.save(genre)

        data = {
            "name": "Anime",
            "is_active": True,
            "categories": [
                str(movie_category.id),
            ],
        }

        url = f"/api/genres/{genre.id}/"
        response = api_client_with_auth.put(
            path=url,
            data=data,
            format="json",
        )

        assert response.status_code == HTTP_204_NO_CONTENT  # type: ignore

        genre_model = genre_repository.get_by_id(genre_id=genre.id)
        assert genre_model == Genre(
            id=genre.id,
            name="Anime",
            is_active=True,
            categories=set(genre_model.categories),  # type: ignore
        )

    def test_when_request_data_is_invalid_then_return_400(
        self,
        genre_repository: DjangoORMGenreRepository,
        movie_category: Category,
        category_repository: DjangoORMCategoryRepository,
        api_client_with_auth: APIClient,
    ):
        """
        Test that the API returns 400 when the given request data is invalid.

        When the API is called with PUT /api/genres/<id>/ and the given request data
        is invalid, it should return a 400 error with a specific error message.

        The expected result is a 400 status code and an error message indicating
        that the genre name can not be blank.
        """

        genre = Genre(name="Romance", is_active=False)
        genre_repository.save(genre)

        data = {
            "name": "",
            "is_active": True,
            "categories": [
                str(movie_category.id),
            ],
        }

        url = f"/api/genres/{genre.id}/"
        response = api_client_with_auth.put(
            path=url,
            data=data,
            format="json",
        )

        assert response.status_code == HTTP_400_BAD_REQUEST  # type: ignore
        assert response.data == {"name": ["This field may not be blank."]}  # type: ignore

    def test_when_related_categories_do_not_exist_then_return_400(
        self,
        genre_repository: DjangoORMGenreRepository,
        api_client_with_auth: APIClient,
    ):
        """
        Test that the API returns 400 when the given request data contains
        a non-existent category ID.

        When the API is called with PUT /api/genres/<id>/ and the given request data
        contains a non-existent category ID, it should return a 400 error with a
        specific error message indicating that the related categories were not found.

        The expected result is a 400 status code and an error message indicating
        that the related categories were not found.
        """

        genre = Genre(name="Horror", is_active=False)
        genre_repository.save(genre)

        data = {
            "name": "Anime",
            "is_active": True,
            "categories": [uuid.uuid4()],
        }

        url = f"/api/genres/{genre.id}/"
        response = api_client_with_auth.put(
            path=url,
            data=data,
            format="json",
        )

        assert response.status_code == HTTP_400_BAD_REQUEST  # type: ignore
        assert response.data == {"error": "Related categories not found"}  # type: ignore

    def test_when_genre_does_not_exist_then_return_404(
        self,
        api_client_with_auth: APIClient,
    ):
        """
        Test that the API returns 404 when attempting to update a genre that does not exist.

        This test sends a PUT request to the /api/genres/<id>/ endpoint with a non-existent
        genre ID. The expected result is a 404 status code and an error message indicating
        that the genre was not found.

        The test verifies that the API correctly handles cases where the specified genre ID
        does not exist in the database.
        """

        data = {
            "name": "Anime",
            "is_active": True,
            "categories": [uuid.uuid4()],
        }

        url = f"/api/genres/{uuid.uuid4()}/"
        response = api_client_with_auth.put(
            path=url,
            data=data,
            format="json",
        )

        assert response.status_code == HTTP_404_NOT_FOUND  # type: ignore
        assert response.data == {"error": "Genre not found"}  # type: ignore
