import uuid
from dataclasses import dataclass
from decimal import Decimal

from src.core._shared.application.use_cases.list import (
    ListRequest,
    ListResponse,
    ListUseCase,
)
from src.core.video.domain.value_objects import Rating
from src.core.video.domain.video_repository import VideoRepository


@dataclass
class VideoWithoutMediaOutput:
    """
    Output data for the list video without media use case.
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


class ListVideoWithoutMedia(ListUseCase):
    """
    List a video by its ID.
    """

    def __init__(self, repository: VideoRepository):
        """
        Initialize the ListVideoWithoutMedia use case.

        Args:
            repository (VideoRepository): The video repository.
        """

        super().__init__(repository)

    def execute(self, request: ListRequest) -> ListResponse:
        """
        Executes the ListVideoWithoutMedia use case to list videos based on request parameters.

        Args:
            request (ListRequest): The request object containing sorting and pagination details.

        Returns:
            ListResponse: A response containing the list of videos and pagination metadata.
        """

        return super().execute(request)
