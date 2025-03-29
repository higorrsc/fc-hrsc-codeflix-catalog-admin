import uuid
from dataclasses import dataclass

from src.core.video.domain.value_objects import MediaType


@dataclass(frozen=True)
class AudioVideoMediaUpdated:
    """
    Event representing the update of an audio/video media.
    """

    aggregate_id: uuid.UUID
    file_path: str
    media_type: MediaType
