import uuid
from dataclasses import dataclass
from pathlib import Path

from src.core._shared.events.abstract_message_bus import AbstractMessageBus
from src.core._shared.infrastructure.storage.abstract_storage_service import (
    AbstractStorageService,
)
from src.core.video.application.events.integration_events import (
    AudioVideoMediaUpdatedIntegrationEvent,
)
from src.core.video.application.exceptions import VideoNotFound
from src.core.video.domain.value_objects import AudioVideoMedia, MediaStatus, MediaType
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
        message_bus: AbstractMessageBus,
    ) -> None:
        """
        Initialize the UploadVideo use case.

        Args:
            video_repository (VideoRepository): The repository to manage video entities.
            storage_service (AbstractStorageService): The storage service to store the
                video media.
            message_bus (AbstractMessageBus): The message bus to publish integration events.
        """

        self.video_repository = video_repository
        self.storage_service = storage_service
        self.message_bus = message_bus

    def execute(self, input: Input) -> None:
        """
        Execute the UploadVideo use case.

        This method uploads video media to a storage service and updates
        the corresponding video entity in the repository. An integration
        event is published after the video is updated.

        Args:
            input (Input): The input data containing the video ID, file name,
                        content, and content type.

        Raises:
            VideoNotFound: If the video with the given ID does not exist.
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
            media_type=MediaType.VIDEO,
        )

        video.update_video(audio_video_media)

        self.video_repository.update(video)

        self.message_bus.handle(
            [
                AudioVideoMediaUpdatedIntegrationEvent(
                    resource_id=f"{video.id}.{MediaType.VIDEO}",
                    file_path=str(file_path),
                )
            ]
        )
