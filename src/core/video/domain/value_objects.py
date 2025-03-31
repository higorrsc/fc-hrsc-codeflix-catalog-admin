from dataclasses import dataclass
from enum import StrEnum, unique


@unique
class ImageType(StrEnum):
    """
    Enumeration representing the type of a image.
    """

    BANNER = "BANNER"
    THUMBNAIL = "THUMBNAIL"
    THUMBNAIL_HALF = "THUMBNAIL_HALF"


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
class MediaType(StrEnum):
    """
    Enumeration representing the type of a media.
    """

    TRAILER = "TRAILER"
    VIDEO = "VIDEO"


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
    image_type: ImageType
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
    media_type: MediaType
    check_sum: str = ""
