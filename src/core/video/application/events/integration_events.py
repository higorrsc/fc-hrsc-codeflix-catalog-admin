from dataclasses import dataclass

from src.core._shared.events.event import Event


@dataclass(frozen=True)
class AudioVideoMediaUpdatedIntegrationEvent(Event):
    """
    Event representing the update of an audio/video media.
    """

    resource_id: str  # <id>.<MediaType>
    file_path: str
