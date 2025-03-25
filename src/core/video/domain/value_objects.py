from dataclasses import dataclass
from enum import Enum, auto, unique


@unique
class MediaStatus(Enum):
    """
    Enumeration representing the status of a media.
    """

    PENDING = auto()
    PROCESSING = auto()
    COMPLETED = auto()
    ERROR = auto()


@unique
class Rating(Enum):
    """
    Enumeration representing the rating of a media.
    """

    ER = auto()
    L = auto()
    AGE_10 = auto()
    AGE_12 = auto()
    AGE_14 = auto()
    AGE_16 = auto()
    AGE_18 = auto()


@dataclass(frozen=True)
class ImageMedia:
    """
    Value object representing an image media.
    """

    check_sum: str
    name: str
    location: str


@dataclass(frozen=True)
class AudioVideoMedia:
    """
    Value object representing an audio or video media.
    """

    check_sum: str
    name: str
    raw_location: str
    encoded_location: str
    status: MediaStatus
