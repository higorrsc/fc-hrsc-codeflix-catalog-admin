import uuid
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

from src.core.video.application.exceptions import VideoNotFound
from src.core.video.domain.value_objects import AudioVideoMedia, ImageMedia, Rating
from src.core.video.domain.video_repository import VideoRepository


class GetVideo:

    @dataclass
    class Input:
        """
        Input data for the GetVideo use case
        """

        id: uuid.UUID

    @dataclass
    class Output:
        """
        Output data for the GetVideo use case
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

        banner: Optional[ImageMedia]
        thumbnail: Optional[ImageMedia]
        thumbnail_half: Optional[ImageMedia]
        trailer: Optional[AudioVideoMedia]
        video: Optional[AudioVideoMedia]

    def __init__(self, repository: VideoRepository) -> None:
        """
        Initialize the GetVideo use case.

        Args:
            repository (VideoRepository): The repository to manage video entities.
        """

        self.repository = repository

    def execute(self, request: Input) -> Output:
        """
        Executes the GetVideo use case to retrieve a video based on its ID.

        Args:
            request (GetVideo.Input): The request object containing the video ID.

        Returns:
            GetVideo.Output: A response containing the video data.

        Raises:
            VideoNotFound: If the video with the given ID does not exist.
        """

        video = self.repository.get_by_id(request.id)

        if not video:
            raise VideoNotFound(f"Video with id {request.id} not found")

        return GetVideo.Output(
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
            banner=video.banner,
            thumbnail=video.thumbnail,
            thumbnail_half=video.thumbnail_half,
            trailer=video.trailer,
            video=video.video,
        )
