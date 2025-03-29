import pytest

from src.config import DEFAULT_PAGE_SIZE
from src.core._shared.application.use_cases.list import (
    ListRequest,
    ListResponse,
    ListResponseMeta,
)
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.category.domain.category import Category
from src.core.genre.domain.genre import Genre
from src.core.video.application.use_cases.list_video_without_media import (
    ListVideoWithoutMedia,
)
from src.core.video.domain.value_objects import Rating
from src.core.video.domain.video import Video
from src.core.video.infra.in_memory_video_repository import InMemoryVideoRepository


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


class TestListGenre:
    """
    Test the ListGenre class.
    """

    def test_list_video_without_media(
        self,
        movie_category: Category,
        documentary_category: Category,
        horror_genre: Genre,
        noir_genre: Genre,
        actor_cast_member: CastMember,
        director_cast_member: CastMember,
    ):
        """
        Test that the ListVideoWithoutMedia use case returns a list of videos
        in the correct order.
        """

        avatar = Video(
            title="Avatar",
            description="""A paraplegic Marine dispatched to the moon Pandora on a
            unique mission becomes torn between following his orders and protecting
            the world he feels is his home.""",
            launch_year=2009,
            duration=162.0,  # type: ignore
            rating=Rating.AGE_12,
            categories={movie_category.id},
            genres={noir_genre.id},
            cast_members={actor_cast_member.id},
        )

        avatar_2 = Video(
            title="Avatar: The Way of Water",
            description="""A paraplegic Marine continues his quest to find out
            the truth about Pandora's world.""",
            launch_year=2022,
            duration=182.0,  # type: ignore
            rating=Rating.AGE_14,
            categories={movie_category.id, documentary_category.id},
            genres={horror_genre.id, noir_genre.id},
            cast_members={actor_cast_member.id, director_cast_member.id},
        )

        repository = InMemoryVideoRepository([avatar, avatar_2])

        use_case = ListVideoWithoutMedia(repository=repository)
        output: ListResponse = use_case.execute(ListRequest(order_by="title"))

        assert output == {
            "data": [
                avatar,
                avatar_2,
            ],
            "meta": ListResponseMeta(
                current_page=1,
                per_page=DEFAULT_PAGE_SIZE,
                total=2,
            ),
        }

    def test_when_no_video_exists_return_empty_list(self):
        """
        Tests that when no video exists in the repository, the ListVideoWithoutMedia
        use case returns an empty list.

        This test verifies that the ListVideoWithoutMedia use case returns an empty list
        when there are no videos in the repository.

        Asserts:
            - The ListVideoWithoutMedia use case returns an empty list.
        """

        repository = InMemoryVideoRepository()

        use_case = ListVideoWithoutMedia(repository=repository)
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
