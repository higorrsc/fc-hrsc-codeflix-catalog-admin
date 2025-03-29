import uuid
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional

from src.core._shared.domain.entity import AbstractEntity
from src.core.video.domain.value_objects import AudioVideoMedia, ImageMedia, Rating


@dataclass(slots=True, kw_only=True)
class Video(AbstractEntity):
    """
    Entity representing a video.
    """

    title: str
    description: str
    launch_year: int
    duration: Decimal
    rating: Rating
    published: bool = field(default=False)

    categories: set[uuid.UUID]
    genres: set[uuid.UUID]
    cast_members: set[uuid.UUID]

    banner: Optional[ImageMedia] = None
    thumbnail: Optional[ImageMedia] = None
    thumbnail_half: Optional[ImageMedia] = None
    trailer: Optional[AudioVideoMedia] = None
    video: Optional[AudioVideoMedia] = None

    def __post_init__(self):
        """
        Validate the video after initialization.

        This method is called automatically after the video is created.
        It validates the video's title.
        """

        self.validate()

    def validate(self) -> None:
        """
        Validate the video.

        Raises:
            ValueError: If the title is empty or longer than 255 characters.
        """

        if not self.title:
            self.notification.add_error("Title cannot be empty")

        if len(self.title) > 255:
            self.notification.add_error("Title must have less than 256 characters")

        if self.notification.has_errors:
            raise ValueError(self.notification.messages)

    def update(
        self,
        title: str,
        description: str,
        launch_year: int,
        duration: Decimal,
        published: bool,
        rating: Rating,
    ) -> None:
        """
        Update the video with the provided attributes.

        Args:
            title (str): The title of the video.
            description (str): The description of the video.
            launch_year (int): The year the video was launched.
            duration (Decimal): The duration of the video in minutes.
            published (bool): Whether the video is published or not.
            rating (Rating): The rating of the video.

        Raises:
            ValueError: If the video data is invalid.
        """

        self.title = title
        self.description = description
        self.launch_year = launch_year
        self.duration = duration
        self.published = published
        self.rating = rating
        self.validate()

    def add_categories(self, category_ids: set[uuid.UUID]) -> None:
        """
        Add multiple categories to the video.

        Args:
            category_ids (set[uuid.UUID]): The IDs of the categories to be added.
        """

        self.categories.update(category_ids)
        self.validate()

    def remove_categories(self, category_ids: set[uuid.UUID]) -> None:
        """
        Remove multiple categories from the video.

        Args:
            category_ids (set[uuid.UUID]): The IDs of the categories to be removed.
        """

        self.categories.difference_update(category_ids)
        self.validate()

    def add_genres(self, genre_ids: set[uuid.UUID]) -> None:
        """
        Add multiple genres to the video.

        Args:
            genre_ids (set[uuid.UUID]): The IDs of the genres to be added.
        """

        self.genres.update(genre_ids)
        self.validate()

    def remove_genres(self, genre_ids: set[uuid.UUID]) -> None:
        """
        Remove multiple genres from the video.

        Args:
            genre_ids (set[uuid.UUID]): The IDs of the genres to be removed.
        """

        self.genres.difference_update(genre_ids)
        self.validate()

    def add_cast_members(self, cast_member_ids: set[uuid.UUID]) -> None:
        """
        Add multiple cast members to the video.

        Args:
            cast_member_ids (set[uuid.UUID]): The IDs of the cast members to be added.
        """

        self.cast_members.update(cast_member_ids)
        self.validate()

    def remove_cast_members(self, cast_member_ids: set[uuid.UUID]) -> None:
        """
        Remove multiple cast members from the video.

        Args:
            cast_member_ids (set[uuid.UUID]): The IDs of the cast members to be removed.
        """

        self.cast_members.difference_update(cast_member_ids)
        self.validate()

    def update_banner(self, banner: ImageMedia) -> None:
        """
        Update the banner of the video.

        Args:
            banner (ImageMedia): The new banner.
        """

        self.banner = banner
        self.validate()

    def update_thumbnail(self, thumbnail: ImageMedia) -> None:
        """
        Update the thumbnail of the video.

        Args:
            thumbnail (ImageMedia): The new thumbnail.
        """

        self.thumbnail = thumbnail
        self.validate()

    def update_thumbnail_half(self, thumbnail_half: ImageMedia) -> None:
        """
        Update the thumbnail half of the video.

        Args:
            thumbnail_half (ImageMedia): The new thumbnail half.
        """

        self.thumbnail_half = thumbnail_half
        self.validate()

    def update_trailer(self, trailer: AudioVideoMedia) -> None:
        """
        Update the trailer of the video.

        Args:
            trailer (AudioVideoMedia): The new trailer.
        """

        self.trailer = trailer
        self.validate()

    def update_video(self, video: AudioVideoMedia) -> None:
        """
        Update the video of the video.

        Args:
            video (AudioVideoMedia): The new video.
        """

        self.video = video
        self.validate()
