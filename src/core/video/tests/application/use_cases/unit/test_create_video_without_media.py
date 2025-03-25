import uuid
from unittest.mock import create_autospec

import pytest

from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository
from src.core.video.application.exceptions import InvalidVideo, RelatedEntitiesNotFound
from src.core.video.application.use_cases.create_video_without_media import (
    CreateVideoWithoutMedia,
)
from src.core.video.domain.value_objects import Rating
from src.core.video.domain.video import Video
from src.core.video.domain.video_repository import VideoRepository


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
def mock_category_repository(category_movie: Category) -> CategoryRepository:
    """
    Fixture for a mock CategoryRepository instance.

    Returns:
        CategoryRepository: A mock CategoryRepository object.
    """

    repository = create_autospec(CategoryRepository)
    repository.list.return_value = [category_movie]
    return repository


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
def mock_genre_repository(
    action_genre: Genre, adventure_genre: Genre
) -> GenreRepository:
    """
    Fixture for a mock GenreRepository instance.

    Returns:
        GenreRepository: A mock GenreRepository object.
    """

    repository = create_autospec(GenreRepository)
    repository.list.return_value = [action_genre, adventure_genre]
    return repository


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
def mock_cast_member_repository(
    actor_cast_member: CastMember,
    director_cast_member: CastMember,
) -> CastMemberRepository:
    """
    Fixture for a mock CastMemberRepository instance.

    Returns:
        CastMemberRepository: A mock CastMemberRepository object with two CastMembers.
    """

    repository = create_autospec(CastMemberRepository)
    repository.list.return_value = [actor_cast_member, director_cast_member]
    return repository


@pytest.fixture
def mock_video_repository(avatar_video: Video) -> VideoRepository:
    """
    Fixture for a mock VideoRepository instance.

    Returns:
        VideoRepository: A mock VideoRepository object.
    """

    repository = create_autospec(VideoRepository)
    repository.list.return_value = [avatar_video]
    return repository


class TesteCreateVideoWithoutMedia:

    def test_create_video_with_valid_data(
        self,
        mock_video_repository: VideoRepository,
        mock_category_repository: CategoryRepository,
        category_movie: Category,
        mock_genre_repository: GenreRepository,
        action_genre: Genre,
        adventure_genre: Genre,
        mock_cast_member_repository: CastMemberRepository,
        actor_cast_member: CastMember,
        director_cast_member: CastMember,
    ):
        """
        When creating a video with valid data, it returns a VideoOutput and saves the Video
        in the repository.

        This test verifies that the `create_video_without_media` use case returns a VideoOutput
        and saves the Video in the provided repository when given valid data.
        """

        use_case = CreateVideoWithoutMedia(
            video_repository=mock_video_repository,
            category_repository=mock_category_repository,
            genre_repository=mock_genre_repository,
            cast_member_repository=mock_cast_member_repository,
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
        assert mock_video_repository.save.call_count == 1  # type: ignore

    def test_create_video_without_valid_data_name_empty(
        self,
        mock_video_repository: VideoRepository,
        mock_category_repository: CategoryRepository,
        mock_genre_repository: GenreRepository,
        mock_cast_member_repository: CastMemberRepository,
    ):
        use_case = CreateVideoWithoutMedia(
            video_repository=mock_video_repository,
            category_repository=mock_category_repository,
            genre_repository=mock_genre_repository,
            cast_member_repository=mock_cast_member_repository,
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
        mock_video_repository: VideoRepository,
        mock_category_repository: CategoryRepository,
        mock_genre_repository: GenreRepository,
        mock_cast_member_repository: CastMemberRepository,
    ):
        """
        When creating a video with valid data and a title longer than 255 characters,
        it raises a InvalidVideo exception.

        This test verifies that the `create_video_without_media` use case raises a
        `InvalidVideo` exception when the given title is longer than 255 characters.
        """

        use_case = CreateVideoWithoutMedia(
            video_repository=mock_video_repository,
            category_repository=mock_category_repository,
            genre_repository=mock_genre_repository,
            cast_member_repository=mock_cast_member_repository,
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
        mock_video_repository: VideoRepository,
        mock_category_repository: CategoryRepository,
        mock_genre_repository: GenreRepository,
        mock_cast_member_repository: CastMemberRepository,
    ):
        """
        When creating a video without valid data and providing an invalid category ID,
        it raises a RelatedEntitiesNotFound exception.

        This test verifies that the `create_video_without_media` use case raises a
        `RelatedEntitiesNotFound` exception when the given category ID does not exist
        in the repository.
        """

        use_case = CreateVideoWithoutMedia(
            video_repository=mock_video_repository,
            category_repository=mock_category_repository,
            genre_repository=mock_genre_repository,
            cast_member_repository=mock_cast_member_repository,
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
        mock_video_repository: VideoRepository,
        mock_category_repository: CategoryRepository,
        mock_genre_repository: GenreRepository,
        mock_cast_member_repository: CastMemberRepository,
    ):
        """
        When creating a video without valid data and providing an invalid genre ID,
        it raises a RelatedEntitiesNotFound exception.

        This test verifies that the `create_video_without_media` use case raises a
        `RelatedEntitiesNotFound` exception when the given genre ID does not exist
        in the repository.
        """

        use_case = CreateVideoWithoutMedia(
            video_repository=mock_video_repository,
            category_repository=mock_category_repository,
            genre_repository=mock_genre_repository,
            cast_member_repository=mock_cast_member_repository,
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
        mock_video_repository: VideoRepository,
        mock_category_repository: CategoryRepository,
        mock_genre_repository: GenreRepository,
        mock_cast_member_repository: CastMemberRepository,
    ):
        """
        Tests that the CreateVideoWithoutMedia use case raises a RelatedEntitiesNotFound
        exception when an invalid cast member ID is provided.

        This test verifies that the `create_video_without_media` use case raises a
        `RelatedEntitiesNotFound` exception when the given cast member ID does not exist
        in the repository.
        """

        use_case = CreateVideoWithoutMedia(
            video_repository=mock_video_repository,
            category_repository=mock_category_repository,
            genre_repository=mock_genre_repository,
            cast_member_repository=mock_cast_member_repository,
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
