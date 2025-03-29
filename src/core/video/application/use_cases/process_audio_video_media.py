import uuid
from dataclasses import dataclass

from src.core.video.application.exceptions import MediaNotFound, VideoNotFound
from src.core.video.domain.value_objects import MediaStatus, MediaType
from src.core.video.domain.video_repository import VideoRepository


class ProcessAudioVideoMedia:
    """
    Use case for processing audio/video media.
    """

    @dataclass
    class Input:
        """
        Input data for the ProcessAudioVideoMedia use case.
        """

        video_id: uuid.UUID
        encoded_location: str
        status: MediaStatus
        media_type: MediaType

    def __init__(self, video_repository: VideoRepository):
        """
        Initialize the ProcessAudioVideoMedia use case.

        Args:
            video_repository (VideoRepository): The repository to manage video entities.
        """

        self.video_repository = video_repository

    def execute(self, request: Input) -> None:
        """
        Execute the ProcessAudioVideoMedia use case.

        Args:
            request (Input): The input data containing the video ID, encoded location,
                status, and media type.

        Raises:
            VideoNotFound: If the video with the given ID does not exist.
            MediaNotFound: If the video does not have media to be processed.
        """

        video = self.video_repository.get_by_id(request.video_id)
        if not video:
            raise VideoNotFound(f"Video with id {request.video_id} not found")

        if request.media_type == MediaType.VIDEO:
            if not video.video:
                raise MediaNotFound("Video must have media to be processed.")

            video.process(
                status=request.status,
                encoded_location=request.encoded_location,
            )

        self.video_repository.update(video)
