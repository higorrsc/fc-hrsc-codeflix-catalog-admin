import uuid
from dataclasses import dataclass
from pathlib import Path

from src.core._shared.infrastructure.storage.abstract_storage_service import (
    AbstractStorageService,
)
from src.core.video.application.exceptions import VideoNotFound
from src.core.video.domain.value_objects import AudioVideoMedia, MediaStatus
from src.core.video.domain.video_repository import VideoRepository


class UploadVideo:
    """
    Use case to upload a video to the storage service and update the video entity.
    """

    @dataclass
    class Input:
        """
        Input for the UploadVideo use case
        """

        video_id: uuid.UUID
        file_name: str
        content: bytes
        content_type: str

    def __init__(
        self,
        video_repository: VideoRepository,
        storage_service: AbstractStorageService,
    ) -> None:
        """
        Initialize the UploadVideo use case.

        Args:
            video_repository (VideoRepository): The repository to manage video entities.
        """

        self.video_repository = video_repository
        self.storage_service = storage_service

    def execute(self, input: Input) -> None:
        """
        Upload a video to the storage service and update the video entity.

        Args:
            input (Input): The input data containing the video ID, file name, content,
                and content type.

        Raises:
            VideoNotFound: If the video with the given ID does not exist
        """

        video = self.video_repository.get_by_id(input.video_id)
        if not video:
            raise VideoNotFound(f"Video with ID {input.video_id} not found")

        file_path = Path("videos") / str(input.video_id) / input.file_name
        self.storage_service.store(
            file_path=str(file_path),
            content=input.content,
            content_type=input.content_type,
        )

        audio_video_media = AudioVideoMedia(
            name=input.file_name,
            raw_location=str(file_path),
            encoded_location="",
            status=MediaStatus.PENDING,
        )

        video.update_video(audio_video_media)

        self.video_repository.update(video)
