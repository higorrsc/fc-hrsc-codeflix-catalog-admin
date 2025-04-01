from dataclasses import dataclass, replace
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

    def _update(self, **changes):
        """
        Returns a new instance with the given changes.

        Args:
            **changes: The changes to apply to the instance.

        Returns:
            A new instance with the given changes.
        """

        return replace(self, **changes)

    def encode_complete(self, encoded_location: str):
        """
        Returns a new instance with the encoded location and status set to COMPLETED.

        Args:
            encoded_location (str): The location of the encoded media.

        Returns:
            A new instance with the given encoded location and status set to COMPLETED.
        """

        return self._update(
            encoded_location=encoded_location,
            status=MediaStatus.COMPLETED,
        )

    def encode_fail(self):
        """
        Returns a new instance with the status set to ERROR.

        Returns:
            A new instance with the status set to ERROR.
        """

        return self._update(status=MediaStatus.ERROR)
