import uuid

import pytest
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.test import APIClient

from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.category.domain.category import Category
from src.core.genre.domain.genre import Genre
from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository
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


@pytest.mark.django_db
class TesteCreateAPI:

    def test_create_video_without_media(
        self,
        movie_category: Category,
        action_genre: Genre,
        adventure_genre: Genre,
        actor_cast_member: CastMember,
        director_cast_member: CastMember,
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

        response = APIClient().post(
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

        response = APIClient().post(
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

        response = APIClient().post(
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
    ):
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

        response = APIClient().post(
            path=url,
            data=data,
            format="json",
        )

        assert response.status_code == HTTP_400_BAD_REQUEST  # type: ignore
        assert "Cast members with provided IDs not found" in response.data["error"]  # type: ignore
