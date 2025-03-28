import uuid
from dataclasses import dataclass
from decimal import Decimal

from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.domain.genre_repository import GenreRepository
from src.core.video.application.exceptions import (
    InvalidVideo,
    RelatedEntitiesNotFound,
    VideoNotFound,
)
from src.core.video.domain.value_objects import Rating
from src.core.video.domain.video_repository import VideoRepository


class UpdateVideoWithoutMedia:
    """
    Use case to update a video without media.
    """

    @dataclass
    class Input:
        """
        Input data for the update video without media use case.
        """

        id: uuid.UUID
        title: str
        description: str
        launch_year: int
        duration: Decimal
        rating: Rating
        published: bool
        categories: set[uuid.UUID]
        genres: set[uuid.UUID]
        cast_members: set[uuid.UUID]

    @dataclass
    class Output:
        """
        Output data for the update video without media use case.
        """

        id: uuid.UUID
        title: str
        description: str
        launch_year: int
        duration: Decimal
        rating: Rating
        published: bool
        categories: set[uuid.UUID]
        genres: set[uuid.UUID]
        cast_members: set[uuid.UUID]

    def __init__(
        self,
        video_repository: VideoRepository,
        category_repository: CategoryRepository,
        genre_repository: GenreRepository,
        cast_member_repository: CastMemberRepository,
    ) -> None:
        """
        Initialize the ListVideoWithoutMedia use case.

        Args:
            video_repository (VideoRepository): The repository to manage video entities.
            category_repository (CategoryRepository): The repository to manage category entities.
            genre_repository (GenreRepository): The repository to manage genre entities.
            cast_member_repository (CastMemberRepository): The repository to manage
            cast member entities.
        """

        self.video_repository = video_repository
        self.category_repository = category_repository
        self.genre_repository = genre_repository
        self.cast_member_repository = cast_member_repository

    def execute(self, input: Input) -> Output:
        """
        Execute the update video without media use case.

        Args:
            input (Input): The input data containing title, description, launch year, duration,
                rating, categories, genres, and cast members.

        Returns:
            Output: The output data with the ID of the created video.

        Raises:
            InvalidVideo: If the video data is invalid.
            VideoNotFound: If the video with the given ID does not exist
        """

        video = self.video_repository.get_by_id(input.id)
        if video is None:
            raise VideoNotFound(f"Video with ID {input.id} not found")

        categories = {category.id for category in self.category_repository.list()}
        if not input.categories.issubset(categories):
            raise RelatedEntitiesNotFound(
                f"Categories with provided IDs not found: {input.categories - categories}"
            )

        genres = {genre.id for genre in self.genre_repository.list()}
        if not input.genres.issubset(genres):
            raise RelatedEntitiesNotFound(
                f"Genres with provided IDs not found: {input.genres - genres}"
            )

        cast_members = {
            cast_member.id for cast_member in self.cast_member_repository.list()
        }
        if not input.cast_members.issubset(cast_members):
            raise RelatedEntitiesNotFound(
                f"Cast members with provided IDs not found: {input.cast_members - cast_members}"
            )

        try:
            video.update(
                title=input.title,
                description=input.description,
                launch_year=input.launch_year,
                duration=input.duration,
                published=input.published,
                rating=input.rating,
            )

            video.categories = input.categories
            video.genres = input.genres
            video.cast_members = input.cast_members

        except ValueError as err:
            raise InvalidVideo(err) from err

        self.video_repository.update(video)

        return self.Output(
            id=video.id,
            title=video.title,
            description=video.description,
            launch_year=video.launch_year,
            duration=video.duration,
            rating=video.rating,
            published=video.published,
            categories=video.categories,
            genres=video.genres,
            cast_members=video.cast_members,
        )
