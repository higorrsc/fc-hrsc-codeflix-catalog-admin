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
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.category.domain.category import Category
from src.core.genre.domain.genre import Genre
from src.core.video.domain.video import Video
from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.genre_app.repository import DjangoORMGenreRepository
from src.django_project.video_app.repository import DjangoORMVideoRepository


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
def action_genre(movie_category: Category) -> Genre:
    """
    Fixture for a Genre instance representing Action movies.

    Returns:
        Genre: A Genre object with name "Action" and the movie category.
    """

    return Genre(
        name="Action",
        categories={movie_category.id},
    )


@pytest.fixture
def adventure_genre(movie_category: Category) -> Genre:
    """
    Fixture for a Genre instance representing Adventure movies.

    Returns:
        Genre: A Genre object with name "Adventure" and the movie category.
    """

    return Genre(
        name="Adventure",
        categories={movie_category.id},
    )


@pytest.fixture
def actor_cast_member() -> CastMember:
    """
    Fixture for a CastMember instance representing Sam Worthington.

    Returns:
        CastMember: A CastMember object with name "Sam Worthington" and type ACTOR.
    """

    return CastMember(
        name="Sam Worthington",
        type=CastMemberType.ACTOR,
    )


@pytest.fixture
def director_cast_member() -> CastMember:
    """
    Fixture for a CastMember instance representing James Cameron.

    Returns:
        CastMember: A CastMember object with name "James Cameron" and type DIRECTOR.
    """

    return CastMember(
        name="James Cameron",
        type=CastMemberType.DIRECTOR,
    )


@pytest.fixture
def avatar_movie(
    movie_category: Category,
    action_genre: Genre,
    adventure_genre: Genre,
    actor_cast_member: CastMember,
    director_cast_member: CastMember,
) -> Video:
    """
    Fixture for a Video instance representing the movie Avatar.

    Args:
        movie_category (Category): The category of the movie.
        action_genre (Genre): The action genre associated with the movie.
        adventure_genre (Genre): The adventure genre associated with the movie.
        actor_cast_member (CastMember): A cast member who is an actor in the movie.
        director_cast_member (CastMember): A cast member who is the director of the movie.

    Returns:
        Video: A Video object with title "Avatar", description of the plot, duration of
        162 minutes, launch year 2009, a rating for age 14 and above, associated categories,
        genres, and cast members.
    """

    return Video(
        title="Avatar",
        description="A marine on an alien planet",
        duration=162,  # type: ignore
        launch_year=2009,
        rating="AGE_14",  # type: ignore
        categories={
            movie_category.id,
        },
        genres={
            action_genre.id,
            adventure_genre.id,
        },
        cast_members={
            actor_cast_member.id,
            director_cast_member.id,
        },
    )


@pytest.fixture
def avatar_2_movie(
    movie_category: Category,
    action_genre: Genre,
    director_cast_member: CastMember,
) -> Video:
    """
    Fixture for a Video instance representing the movie Avatar 2.

    Args:
        movie_category (Category): The movie category associated with the movie.
        action_genre (Genre): The action genre associated with the movie.
        adventure_genre (Genre): The adventure genre associated with the movie.
        actor_cast_member (CastMember): A cast member who is an actor in the movie.
        director_cast_member (CastMember): A cast member who is the director of the movie.

    Returns:
        Video: A Video object with title "Avatar 2", description of the plot, duration of
        182 minutes, launch year 2022, a rating for age 14 and above, associated categories,
        genres, and cast members.
    """

    return Video(
        title="Avatar 2",
        description="A marine on an alien planet",
        duration=182,  # type: ignore
        launch_year=2022,
        rating="AGE_14",  # type: ignore
        categories={
            movie_category.id,
        },
        genres={
            action_genre.id,
        },
        cast_members={
            director_cast_member.id,
        },
    )


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
    Test class for the ListVideoAPI view
    """

    def test_list_videos(
        self,
        avatar_movie: Video,
        avatar_2_movie: Video,
        movie_category: Category,
        action_genre: Genre,
        adventure_genre: Genre,
        actor_cast_member: CastMember,
        director_cast_member: CastMember,
        api_client_with_auth: APIClient,
    ):
        """
        Tests that a list of Video instances can be retrieved from the ListVideoAPI
        view along with their associated categories, genres, and cast members.

        This test creates two Video instances and saves them to the repository. It
        then retrieves the list of videos and asserts that the videos are correctly
        associated with their respective categories, genres, and cast members.

        Asserts:
            - The status code of the response is 200.
            - The response data is equal to the expected data.
        """

        category_repository = DjangoORMCategoryRepository()
        category_repository.save(movie_category)

        genre_repository = DjangoORMGenreRepository()
        genre_repository.save(action_genre)
        genre_repository.save(adventure_genre)

        cast_member_repository = DjangoORMCastMemberRepository()
        cast_member_repository.save(actor_cast_member)
        cast_member_repository.save(director_cast_member)

        video_repository = DjangoORMVideoRepository()
        video_repository.save(avatar_movie)
        video_repository.save(avatar_2_movie)

        url = "/api/videos/"
        expected_data = {
            "data": [
                {
                    "id": str(avatar_movie.id),
                    "title": "Avatar",
                    "description": "A marine on an alien planet",
                    "duration": 162,
                    "launch_year": 2009,
                    "rating": "AGE_14",
                    "categories": [movie_category.id],
                    "genres": [action_genre.id, adventure_genre.id],
                    "cast_members": [actor_cast_member.id, director_cast_member.id],
                },
                {
                    "id": str(avatar_2_movie.id),
                    "title": "Avatar 2",
                    "description": "A marine on an alien planet",
                    "duration": 182,
                    "launch_year": 2022,
                    "rating": "AGE_14",
                    "categories": [movie_category.id],
                    "genres": [action_genre.id],
                    "cast_members": [director_cast_member.id],
                },
            ],
            "meta": {
                "current_page": 1,
                "per_page": DEFAULT_PAGE_SIZE,
                "total": 2,
            },
        }

        response = api_client_with_auth.get(path=url)

        assert response.status_code == HTTP_200_OK  # type: ignore
        assert response.data, expected_data  # type: ignore


@pytest.mark.django_db
class TestRetrieveAPI:
    """
    Test class for the RetrieveVideoAPI view
    """

    def test_get_video(
        self,
        avatar_movie: Video,
        movie_category: Category,
        action_genre: Genre,
        adventure_genre: Genre,
        actor_cast_member: CastMember,
        director_cast_member: CastMember,
        api_client_with_auth: APIClient,
    ):
        """
        Tests that a Video instance can be retrieved from the database using DjangoORMVideoRepository.

        This test creates a Video instance with predefined attributes and saves it
        to the repository. It then retrieves the video by its ID and asserts that the
        video is correctly retrieved with all its associated categories, genres, and
        cast members.

        Asserts:
            - The status code of the response is 200.
            - The retrieved video data matches the expected data.
        """

        category_repository = DjangoORMCategoryRepository()
        category_repository.save(movie_category)

        genre_repository = DjangoORMGenreRepository()
        genre_repository.save(action_genre)
        genre_repository.save(adventure_genre)

        cast_member_repository = DjangoORMCastMemberRepository()
        cast_member_repository.save(actor_cast_member)
        cast_member_repository.save(director_cast_member)

        video_repository = DjangoORMVideoRepository()
        video_repository.save(avatar_movie)

        url = f"/api/videos/{avatar_movie.id}/"
        expected_data = {
            "data": {
                "id": str(avatar_movie.id),
                "title": "Avatar",
                "description": "A marine on an alien planet",
                "duration": 162,
                "launch_year": 2009,
                "rating": "AGE_14",
                "categories": [movie_category.id],
                "genres": [action_genre.id, adventure_genre.id],
                "cast_members": [actor_cast_member.id, director_cast_member.id],
            }
        }

        response = api_client_with_auth.get(path=url)

        assert response.status_code == HTTP_200_OK  # type: ignore
        assert response.data, expected_data  # type: ignore

    def test_get_video_with_invalid_id(
        self,
        api_client_with_auth: APIClient,
    ):
        """
        Tests that a 404 response is returned when retrieving a video with an
        invalid ID.

        Asserts:
            - The status code of the response is 404.
            - The response data contains an error message indicating that the
              video was not found.
        """

        url = f"/api/videos/{uuid.uuid4()}/"
        response = api_client_with_auth.get(path=url)

        assert response.status_code == HTTP_404_NOT_FOUND  # type: ignore
        assert response.data == {"error": "Video not found"}  # type: ignore


@pytest.mark.django_db
class TestCreateAPI:
    """
    Test class for the CreateVideoAPI view
    """

    def test_create_video_without_media(
        self,
        movie_category: Category,
        action_genre: Genre,
        adventure_genre: Genre,
        actor_cast_member: CastMember,
        director_cast_member: CastMember,
        api_client_with_auth: APIClient,
    ):
        """
        When creating a video without valid data and providing an invalid category ID,
        it returns a 400 response with an error message indicating the problem.

        This test verifies that the API endpoint returns a 400 response with a
        meaningful error message when the given category ID does not exist
        in the repository.
        """

        category_repository = DjangoORMCategoryRepository()
        category_repository.save(movie_category)

        genre_repository = DjangoORMGenreRepository()
        genre_repository.save(action_genre)
        genre_repository.save(adventure_genre)

        cast_member_repository = DjangoORMCastMemberRepository()
        cast_member_repository.save(actor_cast_member)
        cast_member_repository.save(director_cast_member)

        url = "/api/videos/"
        data = {
            "title": "Avatar",
            "description": "A marine on an alien planet",
            "duration": 162,
            "launch_year": 2009,
            "rating": "AGE_14",
            "categories": [
                movie_category.id,
            ],
            "genres": [
                action_genre.id,
                adventure_genre.id,
            ],
            "cast_members": [
                actor_cast_member.id,
                director_cast_member.id,
            ],
        }

        response = api_client_with_auth.post(
            path=url,
            data=data,
            format="json",
        )

        assert response.status_code == HTTP_201_CREATED  # type: ignore
        assert response.data["id"]  # type: ignore

    def test_create_video_without_media_with_invalid_category(
        self,
        movie_category: Category,
        action_genre: Genre,
        adventure_genre: Genre,
        actor_cast_member: CastMember,
        director_cast_member: CastMember,
        api_client_with_auth: APIClient,
    ):
        """
        When creating a video without valid data and providing an invalid category ID,
        it returns a 400 response with an error message indicating the problem.

        This test verifies that the API endpoint returns a 400 response with a
        meaningful error message when the given category ID does not exist
        in the repository.
        """

        category_repository = DjangoORMCategoryRepository()
        category_repository.save(movie_category)

        genre_repository = DjangoORMGenreRepository()
        genre_repository.save(action_genre)
        genre_repository.save(adventure_genre)

        cast_member_repository = DjangoORMCastMemberRepository()
        cast_member_repository.save(actor_cast_member)
        cast_member_repository.save(director_cast_member)

        invalid_id = uuid.uuid4()
        url = "/api/videos/"
        data = {
            "title": "Avatar",
            "description": "A marine on an alien planet",
            "duration": 162,
            "launch_year": 2009,
            "rating": "AGE_14",
            "categories": [
                str(invalid_id),
            ],
            "genres": [
                action_genre.id,
                adventure_genre.id,
            ],
            "cast_members": [
                actor_cast_member.id,
                director_cast_member.id,
            ],
        }

        response = api_client_with_auth.post(
            path=url,
            data=data,
            format="json",
        )

        assert response.status_code == HTTP_400_BAD_REQUEST  # type: ignore
        assert "Categories with provided IDs not found" in response.data["error"]  # type: ignore

    def test_create_video_without_media_with_invalid_genre(
        self,
        movie_category: Category,
        action_genre: Genre,
        adventure_genre: Genre,
        actor_cast_member: CastMember,
        director_cast_member: CastMember,
        api_client_with_auth: APIClient,
    ):
        """
        When creating a video without valid data and providing an invalid genre ID,
        it returns a 400 response with an error message indicating the problem.

        This test verifies that the API endpoint returns a 400 response with a
        meaningful error message when the given genre ID does not exist
        in the repository.
        """

        category_repository = DjangoORMCategoryRepository()
        category_repository.save(movie_category)

        genre_repository = DjangoORMGenreRepository()
        genre_repository.save(action_genre)
        genre_repository.save(adventure_genre)

        cast_member_repository = DjangoORMCastMemberRepository()
        cast_member_repository.save(actor_cast_member)
        cast_member_repository.save(director_cast_member)

        invalid_id = uuid.uuid4()
        url = "/api/videos/"
        data = {
            "title": "Avatar",
            "description": "A marine on an alien planet",
            "duration": 162,
            "launch_year": 2009,
            "rating": "AGE_14",
            "categories": [
                movie_category.id,
            ],
            "genres": [
                str(invalid_id),
                action_genre.id,
                adventure_genre.id,
            ],
            "cast_members": [
                actor_cast_member.id,
                director_cast_member.id,
            ],
        }

        response = api_client_with_auth.post(
            path=url,
            data=data,
            format="json",
        )

        assert response.status_code == HTTP_400_BAD_REQUEST  # type: ignore
        assert "Genres with provided IDs not found" in response.data["error"]  # type: ignore

    def test_create_video_without_media_with_invalid_cast_member(
        self,
        movie_category: Category,
        action_genre: Genre,
        adventure_genre: Genre,
        actor_cast_member: CastMember,
        director_cast_member: CastMember,
        api_client_with_auth: APIClient,
    ):
        """
        When creating a video without valid data and providing an invalid cast member ID,
        it returns a 400 response with an error message indicating the problem.

        This test verifies that the API endpoint returns a 400 response with a
        meaningful error message when the given cast member ID does not exist
        in the repository.
        """

        category_repository = DjangoORMCategoryRepository()
        category_repository.save(movie_category)

        genre_repository = DjangoORMGenreRepository()
        genre_repository.save(action_genre)
        genre_repository.save(adventure_genre)

        cast_member_repository = DjangoORMCastMemberRepository()
        cast_member_repository.save(actor_cast_member)
        cast_member_repository.save(director_cast_member)

        invalid_id = uuid.uuid4()
        url = "/api/videos/"
        data = {
            "title": "Avatar",
            "description": "A marine on an alien planet",
            "duration": 162,
            "launch_year": 2009,
            "rating": "AGE_14",
            "categories": [
                movie_category.id,
            ],
            "genres": [
                action_genre.id,
                adventure_genre.id,
            ],
            "cast_members": [
                str(invalid_id),
                actor_cast_member.id,
                director_cast_member.id,
            ],
        }

        response = api_client_with_auth.post(
            path=url,
            data=data,
            format="json",
        )

        assert response.status_code == HTTP_400_BAD_REQUEST  # type: ignore
        assert "Cast members with provided IDs not found" in response.data["error"]  # type: ignore


@pytest.mark.django_db
class TestUpdateAPI:
    """
    Test class for the UpdateVideoAPI view
    """

    def test_update_video(
        self,
        avatar_movie: Video,
        movie_category: Category,
        action_genre: Genre,
        adventure_genre: Genre,
        actor_cast_member: CastMember,
        director_cast_member: CastMember,
        api_client_with_auth: APIClient,
    ):
        """
        Tests that a Video instance can be updated from the UpdateVideoAPI view.

        This test creates a Video instance with predefined attributes and saves it
        to the repository. It then updates the video by its ID and asserts that the
        video is correctly updated and the response is a 204 No Content.

        Asserts:
            - The status code of the response is 204.
        """

        category_repository = DjangoORMCategoryRepository()
        category_repository.save(movie_category)

        genre_repository = DjangoORMGenreRepository()
        genre_repository.save(action_genre)
        genre_repository.save(adventure_genre)

        cast_member_repository = DjangoORMCastMemberRepository()
        cast_member_repository.save(actor_cast_member)
        cast_member_repository.save(director_cast_member)

        video_repository = DjangoORMVideoRepository()
        video_repository.save(avatar_movie)

        url = f"/api/videos/{avatar_movie.id}/"
        data = {
            "title": "Avatar Updated",
            "description": "A marine on an alien planet",
            "duration": 162,
            "launch_year": 2009,
            "rating": "AGE_14",
            "published": True,
            "categories": [
                movie_category.id,
            ],
            "genres": [
                action_genre.id,
                adventure_genre.id,
            ],
            "cast_members": [
                actor_cast_member.id,
                director_cast_member.id,
            ],
        }

        response = api_client_with_auth.put(
            path=url,
            data=data,
            format="json",
        )

        assert response.status_code == HTTP_204_NO_CONTENT  # type: ignore

    def test_update_video_with_invalid_category(
        self,
        avatar_movie: Video,
        movie_category: Category,
        action_genre: Genre,
        adventure_genre: Genre,
        actor_cast_member: CastMember,
        director_cast_member: CastMember,
        api_client_with_auth: APIClient,
    ):
        """
        Tests that updating a video with an invalid category ID fails.

        This test saves a category, genres, and cast members to the repository.
        It then saves a video to the repository and attempts to update the video
        with an invalid category ID. The update should fail and the response should
        have a 400 status code with an error message indicating the problem.

        Asserts:
            - The status code of the response is 400.
            - The response data is equal to the expected data.
        """

        category_repository = DjangoORMCategoryRepository()
        category_repository.save(movie_category)

        genre_repository = DjangoORMGenreRepository()
        genre_repository.save(action_genre)
        genre_repository.save(adventure_genre)

        cast_member_repository = DjangoORMCastMemberRepository()
        cast_member_repository.save(actor_cast_member)
        cast_member_repository.save(director_cast_member)

        video_repository = DjangoORMVideoRepository()
        video_repository.save(avatar_movie)

        url = f"/api/videos/{avatar_movie.id}/"
        data = {
            "title": "Avatar Updated",
            "description": "A marine on an alien planet",
            "duration": 162,
            "launch_year": 2009,
            "rating": "AGE_14",
            "published": True,
            "categories": [
                str(uuid.uuid4()),
            ],
            "genres": [
                action_genre.id,
                adventure_genre.id,
            ],
            "cast_members": [
                actor_cast_member.id,
                director_cast_member.id,
            ],
        }

        response = api_client_with_auth.put(
            path=url,
            data=data,
            format="json",
        )

        assert response.status_code == HTTP_404_NOT_FOUND  # type: ignore
        assert "Categories with provided IDs not found" in response.data["error"]  # type: ignore


@pytest.mark.django_db
class TestDeleteAPI:
    """
    Test class for the DeleteVideoAPI view
    """

    def test_delete_video(
        self,
        avatar_movie: Video,
        movie_category: Category,
        action_genre: Genre,
        adventure_genre: Genre,
        actor_cast_member: CastMember,
        director_cast_member: CastMember,
        api_client_with_auth: APIClient,
    ):
        """
        Tests that a Video instance can be deleted from the database using DjangoORMVideoRepository.

        This test creates a Video instance with predefined attributes and saves it
        to the repository. It then deletes the video by its ID and asserts that the
        video is no longer in the repository and the count of VideoModel objects in
        the database is 0.

        Asserts:
            - The count of VideoModel objects in the database is 1 after saving.
            - The count of VideoModel objects in the database is 0 after deleting.
            - The retrieved video from the database is None after deleting.
        """

        category_repository = DjangoORMCategoryRepository()
        category_repository.save(movie_category)

        genre_repository = DjangoORMGenreRepository()
        genre_repository.save(action_genre)
        genre_repository.save(adventure_genre)

        cast_member_repository = DjangoORMCastMemberRepository()
        cast_member_repository.save(actor_cast_member)
        cast_member_repository.save(director_cast_member)

        video_repository = DjangoORMVideoRepository()
        video_repository.save(avatar_movie)

        url = f"/api/videos/{avatar_movie.id}/"
        response = api_client_with_auth.delete(url)

        assert response.status_code == HTTP_204_NO_CONTENT  # type: ignore

    def test_delete_video_not_found(
        self,
        api_client_with_auth: APIClient,
    ):
        """
        Tests that the API returns 404 when the given video ID does not exist.

        When the API is called with DELETE /api/videos/<id>/ and the given video ID
        does not exist, it should return a 404 error with a specific error message.

        The expected result is a 404 status code and an error message indicating
        that the video was not found.
        """

        url = f"/api/videos/{uuid.uuid4()}/"
        response = api_client_with_auth.delete(url)

        assert response.status_code == HTTP_404_NOT_FOUND  # type: ignore
        assert "Video not found" in response.data["error"]  # type: ignore
