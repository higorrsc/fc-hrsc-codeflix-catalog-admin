from dataclasses import dataclass
from enum import StrEnum, unique


@unique
class MediaStatus(StrEnum):
    """
    Enumeration representing the status of a media.
    """

    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    ERROR = "ERROR"


@unique
class Rating(StrEnum):
    """
    Enumeration representing the rating of a media.
    """

    ER = "ER"
    L = "L"
    AGE_10 = "AGE_10"
    AGE_12 = "AGE_12"
    AGE_14 = "AGE_14"
    AGE_16 = "AGE_16"
    AGE_18 = "AGE_18"


@dataclass(frozen=True)
class ImageMedia:
    """
    Value object representing an image media.
    """

    name: str
    location: str
    check_sum: str = ""


@dataclass(frozen=True)
class AudioVideoMedia:
    """
    Value object representing an audio or video media.
    """

    name: str
    raw_location: str
    encoded_location: str
    status: MediaStatus
    check_sum: str = ""
