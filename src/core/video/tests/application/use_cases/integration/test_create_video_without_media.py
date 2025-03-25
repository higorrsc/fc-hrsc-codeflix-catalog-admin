import uuid

import pytest

from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.core.cast_member.infra.in_memory_cast_member_repository import (
    InMemoryCastMemberRepository,
)
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
)
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository
from src.core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository
from src.core.video.application.exceptions import InvalidVideo, RelatedEntitiesNotFound
from src.core.video.application.use_cases.create_video_without_media import (
    CreateVideoWithoutMedia,
)
from src.core.video.domain.value_objects import Rating
from src.core.video.domain.video import Video
from src.core.video.infra.in_memory_video_repository import InMemoryVideoRepository


@pytest.fixture
def category_movie() -> Category:
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
def category_repository(category_movie: Category) -> CategoryRepository:
    """
    Fixture for a mock CategoryRepository instance.

    Returns:
        CategoryRepository: A mock CategoryRepository object.
    """

    return InMemoryCategoryRepository([category_movie])


@pytest.fixture
def action_genre(category_movie: Category) -> Genre:
    """
    Fixture for a Genre instance representing Action movies.

    Returns:
        Genre: A Genre object with name "Action" and the movie category.
    """

    return Genre(
        name="Action",
        categories={category_movie.id},
    )


@pytest.fixture
def adventure_genre(category_movie: Category) -> Genre:
    """
    Fixture for a Genre instance representing Adventure movies.

    Returns:
        Genre: A Genre object with name "Adventure" and the movie category.
    """

    return Genre(
        name="Adventure",
        categories={category_movie.id},
    )


@pytest.fixture
def genre_repository(action_genre: Genre, adventure_genre: Genre) -> GenreRepository:
    """
    Fixture for a mock GenreRepository instance.

    Returns:
        GenreRepository: A mock GenreRepository object.
    """

    return InMemoryGenreRepository(
        [
            action_genre,
            adventure_genre,
        ]
    )


@pytest.fixture
def avatar_video() -> Video:
    """
    Fixture for a Video instance representing the movie Avatar.

    Returns:
        Video: A Video object with title "Avatar", description of the movie
        plot, duration of 162 minutes, launch year 2009, unpublished status,
        rating for age 12 and above, no categories, four genres,
        and twenty cast members.
    """

    return Video(
        title="Avatar",
        description="""A paraplegic Marine dispatched to the moon Pandora on a
        unique mission becomes torn between following his orders and protecting
        the world he feels is his home.""",
        duration=162.0,  # type: ignore
        launch_year=2009,
        published=False,
        rating=Rating.AGE_12,
        categories=set(),
        genres=set(),
        cast_members=set(),
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
def cast_member_repository(
    actor_cast_member: CastMember,
    director_cast_member: CastMember,
) -> CastMemberRepository:
    """
    Fixture for a mock CastMemberRepository instance.

    Returns:
        CastMemberRepository: A mock CastMemberRepository object with two CastMembers.
    """

    return InMemoryCastMemberRepository(
        [
            actor_cast_member,
            director_cast_member,
        ]
    )


class TesteCreateVideoWithoutMedia:

    def test_create_video_with_valid_data(
        self,
        category_repository: CategoryRepository,
        category_movie: Category,
        genre_repository: GenreRepository,
        action_genre: Genre,
        adventure_genre: Genre,
        cast_member_repository: CastMemberRepository,
        actor_cast_member: CastMember,
        director_cast_member: CastMember,
    ):

        repository = InMemoryVideoRepository()
        use_case = CreateVideoWithoutMedia(
            video_repository=repository,
            category_repository=category_repository,
            genre_repository=genre_repository,
            cast_member_repository=cast_member_repository,
        )

        result = use_case.execute(
            CreateVideoWithoutMedia.Input(
                title="Avatar",
                description="""A paraplegic Marine dispatched to the moon Pandora on a
                unique mission becomes torn between following his orders and protecting
                the world he feels is his home.""",
                launch_year=2009,
                duration=162.0,  # type: ignore
                rating=Rating.AGE_12,
                categories={category_movie.id},
                genres={action_genre.id, adventure_genre.id},
                cast_members={actor_cast_member.id, director_cast_member.id},
            )
        )
        assert isinstance(result.id, uuid.UUID)
        saved_video = repository.get_by_id(result.id)

        assert saved_video.title == "Avatar"  # type: ignore
        assert (
            saved_video.description  # type: ignore
            == """A paraplegic Marine dispatched to the moon Pandora on a
                unique mission becomes torn between following his orders and protecting
                the world he feels is his home."""
        )
        assert saved_video.duration == 162.0  # type: ignore
        assert saved_video.launch_year == 2009  # type: ignore
        assert saved_video.published is False  # type: ignore
        assert saved_video.rating == Rating.AGE_12  # type: ignore
        assert saved_video.categories == {category_movie.id}  # type: ignore
        assert saved_video.genres == {action_genre.id, adventure_genre.id}  # type: ignore
        assert saved_video.cast_members == {actor_cast_member.id, director_cast_member.id}  # type: ignore

    def test_create_video_without_valid_data_name_empty(
        self,
        category_repository: CategoryRepository,
        genre_repository: GenreRepository,
        cast_member_repository: CastMemberRepository,
    ):
        repository = InMemoryVideoRepository()
        use_case = CreateVideoWithoutMedia(
            video_repository=repository,
            category_repository=category_repository,
            genre_repository=genre_repository,
            cast_member_repository=cast_member_repository,
        )

        with pytest.raises(InvalidVideo) as exc_info:
            use_case.execute(
                CreateVideoWithoutMedia.Input(
                    title="",
                    description="""A paraplegic Marine dispatched to the moon Pandora on a
                    unique mission becomes torn between following his orders and protecting
                    the world he feels is his home.""",
                    launch_year=2009,
                    duration=162.0,  # type: ignore
                    rating=Rating.AGE_12,
                    categories=set(),
                    genres=set(),
                    cast_members=set(),
                )
            )

        assert "Title cannot be empty" in str(exc_info.value)

    def test_create_video_without_valid_data_name_longer_than_255_characters(
        self,
        category_repository: CategoryRepository,
        genre_repository: GenreRepository,
        cast_member_repository: CastMemberRepository,
    ):
        repository = InMemoryVideoRepository()
        use_case = CreateVideoWithoutMedia(
            video_repository=repository,
            category_repository=category_repository,
            genre_repository=genre_repository,
            cast_member_repository=cast_member_repository,
        )

        with pytest.raises(InvalidVideo) as exc_info:
            use_case.execute(
                CreateVideoWithoutMedia.Input(
                    title="A" * 256,
                    description="""A paraplegic Marine dispatched to the moon Pandora on a
                    unique mission becomes torn between following his orders and protecting
                    the world he feels is his home.""",
                    launch_year=2009,
                    duration=162.0,  # type: ignore
                    rating=Rating.AGE_12,
                    categories=set(),
                    genres=set(),
                    cast_members=set(),
                )
            )

        assert "Title must have less than 256 characters" in str(exc_info.value)

    def test_create_video_without_valid_data_invalid_category_id(
        self,
        category_repository: CategoryRepository,
        genre_repository: GenreRepository,
        cast_member_repository: CastMemberRepository,
    ):
        """
        When creating a video without valid data and providing an invalid category ID,
        it raises a RelatedEntitiesNotFound exception.

        This test verifies that the `create_video_without_media` use case raises a
        `RelatedEntitiesNotFound` exception when the given category ID does not exist
        in the repository.
        """

        repository = InMemoryVideoRepository()
        use_case = CreateVideoWithoutMedia(
            video_repository=repository,
            category_repository=category_repository,
            genre_repository=genre_repository,
            cast_member_repository=cast_member_repository,
        )

        invalid_id = uuid.uuid4()

        with pytest.raises(RelatedEntitiesNotFound) as exc_info:
            use_case.execute(
                CreateVideoWithoutMedia.Input(
                    title="Avatar",
                    description="""A paraplegic Marine dispatched to the moon Pandora on a
                    unique mission becomes torn between following his orders and protecting
                    the world he feels is his home.""",
                    launch_year=2009,
                    duration=162.0,  # type: ignore
                    rating=Rating.AGE_12,
                    categories={invalid_id},
                    genres=set(),
                    cast_members=set(),
                )
            )

        assert "Categories with provided IDs not found:" in str(exc_info.value)

    def test_create_video_without_valid_data_invalid_genre_id(
        self,
        category_repository: CategoryRepository,
        genre_repository: GenreRepository,
        cast_member_repository: CastMemberRepository,
    ):
        """
        When creating a video without valid data and providing an invalid genre ID,
        it raises a RelatedEntitiesNotFound exception.

        This test verifies that the `create_video_without_media` use case raises a
        `RelatedEntitiesNotFound` exception when the given genre ID does not exist
        in the repository.
        """

        repository = InMemoryVideoRepository()
        use_case = CreateVideoWithoutMedia(
            video_repository=repository,
            category_repository=category_repository,
            genre_repository=genre_repository,
            cast_member_repository=cast_member_repository,
        )

        invalid_id = uuid.uuid4()

        with pytest.raises(RelatedEntitiesNotFound) as exc_info:
            use_case.execute(
                CreateVideoWithoutMedia.Input(
                    title="Avatar",
                    description="""A paraplegic Marine dispatched to the moon Pandora on a
                    unique mission becomes torn between following his orders and protecting
                    the world he feels is his home.""",
                    launch_year=2009,
                    duration=162.0,  # type: ignore
                    rating=Rating.AGE_12,
                    categories=set(),
                    genres={invalid_id},
                    cast_members=set(),
                )
            )

        assert "Genres with provided IDs not found:" in str(exc_info.value)

    def test_create_video_without_valid_data_invalid_cast_member_id(
        self,
        category_repository: CategoryRepository,
        genre_repository: GenreRepository,
        cast_member_repository: CastMemberRepository,
    ):
        """
        Tests that the CreateVideoWithoutMedia use case raises a RelatedEntitiesNotFound
        exception when an invalid cast member ID is provided.

        This test verifies that the `create_video_without_media` use case raises a
        `RelatedEntitiesNotFound` exception when the given cast member ID does not exist
        in the repository.
        """

        repository = InMemoryVideoRepository()
        use_case = CreateVideoWithoutMedia(
            video_repository=repository,
            category_repository=category_repository,
            genre_repository=genre_repository,
            cast_member_repository=cast_member_repository,
        )

        invalid_id = uuid.uuid4()

        with pytest.raises(RelatedEntitiesNotFound) as exc_info:
            use_case.execute(
                CreateVideoWithoutMedia.Input(
                    title="Avatar",
                    description="""A paraplegic Marine dispatched to the moon Pandora on a
                    unique mission becomes torn between following his orders and protecting
                    the world he feels is his home.""",
                    launch_year=2009,
                    duration=162.0,  # type: ignore
                    rating=Rating.AGE_12,
                    categories=set(),
                    genres=set(),
                    cast_members={invalid_id},
                )
            )

        assert "Cast members with provided IDs not found:" in str(exc_info.value)
