import uuid
from dataclasses import dataclass
from decimal import Decimal

from src.core._shared.notification import Notification
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.domain.genre_repository import GenreRepository
from src.core.video.application.exceptions import InvalidVideo, RelatedEntitiesNotFound
from src.core.video.domain.value_objects import Rating
from src.core.video.domain.video import Video
from src.core.video.domain.video_repository import VideoRepository


class CreateVideoWithoutMedia:
    """
    Use case to create a video without media.
    """

    @dataclass
    class Input:
        """
        Input data for the create video without media use case.
        """

        title: str
        description: str
        launch_year: int
        duration: Decimal
        rating: Rating
        categories: set[uuid.UUID]
        genres: set[uuid.UUID]
        cast_members: set[uuid.UUID]

    @dataclass
    class Output:
        """
        Output data for the create video without media use case.
        """

        id: uuid.UUID

    def __init__(
        self,
        video_repository: VideoRepository,
        category_repository: CategoryRepository,
        genre_repository: GenreRepository,
        cast_member_repository: CastMemberRepository,
    ) -> None:
        """
        Initialize the CreateVideoWithoutMedia use case.

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
        Execute the CreateVideoWithoutMedia use case.

        Args:
            input (Input): The input data containing title, description, launch year, duration,
                rating, categories, genres, and cast members.

        Returns:
            Output: The output data with the ID of the created video.

        Raises:
            InvalidVideo: If the video data is invalid.
            RelatedEntitiesNotFound: If any related entities (categories, genres, or cast members)
                are not found.
        """
        notification = Notification()

        self.__validate_categories(input, notification)
        self.__validate_genres(input, notification)
        self.__validate_cast_members(input, notification)

        if notification.has_errors:
            raise RelatedEntitiesNotFound(notification.messages)

        try:
            video = Video(
                title=input.title,
                description=input.description,
                launch_year=input.launch_year,
                duration=input.duration,
                published=False,
                rating=input.rating,
                categories=input.categories,
                genres=input.genres,
                cast_members=input.cast_members,
            )
        except ValueError as error:
            raise InvalidVideo(error) from error

        self.video_repository.save(video)

        return self.Output(id=video.id)

    def __validate_categories(self, input: Input, notification: Notification) -> None:
        """
        Validate the categories in the input.

        Args:
            input (Input): The input data containing category IDs.
            notification (Notification): The notification object to collect validation errors.

        Adds an error to the notification if any category IDs in the input are not
        present in the category repository.
        """

        categories = {category.id for category in self.category_repository.list()}
        if not input.categories.issubset(categories):
            notification.add_error(
                f"Categories with provided IDs not found: {input.categories - categories}"
            )

    def __validate_genres(self, input: Input, notification: Notification) -> None:
        """
        Validate the genres in the input.

        Args:
            input (Input): The input data containing genre IDs.
            notification (Notification): The notification object to collect validation errors.

        Adds an error to the notification if any genre IDs in the input are not
        present in the genre repository.
        """

        genres = {genre.id for genre in self.genre_repository.list()}
        if not input.genres.issubset(genres):
            notification.add_error(
                f"Genres with provided IDs not found: {input.genres - genres}"
            )

    def __validate_cast_members(self, input: Input, notification: Notification) -> None:
        """
        Validate the cast members in the input.

        Args:
            input (Input): The input data containing cast member IDs.
            notification (Notification): The notification object to collect validation errors.

        Adds an error to the notification if any cast member IDs in the input are not
        present in the cast member repository.
        """

        cast_members = {
            cast_member.id for cast_member in self.cast_member_repository.list()
        }
        if not input.cast_members.issubset(cast_members):
            notification.add_error(
                f"Cast members with provided IDs not found: {input.cast_members - cast_members}"
            )
