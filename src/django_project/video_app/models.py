import uuid

from django.db import models

from src.core.video.domain.value_objects import (
    ImageType,
    MediaStatus,
    MediaType,
    Rating,
)


class Video(models.Model):
    """
    Model representing a video.
    """

    RATING_CHOICES = [(rating.name, rating.name) for rating in Rating]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    launch_year = models.IntegerField()
    duration = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    published = models.BooleanField(
        default=False,
        null=False,
        blank=False,
    )
    rating = models.CharField(
        max_length=10,
        choices=RATING_CHOICES,
    )

    categories = models.ManyToManyField(
        "category_app.Category",
        related_name="videos",
    )
    genres = models.ManyToManyField(
        "genre_app.Genre",
        related_name="videos",
    )
    cast_members = models.ManyToManyField(
        "cast_member_app.CastMember",
        related_name="videos",
    )

    banner = models.OneToOneField(
        "ImageMedia",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="video_banner",
    )
    thumbnail = models.OneToOneField(
        "ImageMedia",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="video_thumbnail",
    )
    thumbnail_half = models.OneToOneField(
        "ImageMedia",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="video_thumbnail_half",
    )
    trailer = models.OneToOneField(
        "AudioVideoMedia",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="video_trailer",
    )
    video = models.OneToOneField(
        "AudioVideoMedia",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="video_video",
    )

    def __str__(self) -> str:
        """
        Return a human-readable string representation of the video.

        Returns:
            str: A human-readable string representation of the video.
        """

        return str(self.title)

    class Meta:
        """
        Meta class for the Video model
        """

        db_table = "video"
        verbose_name = "Video"
        verbose_name_plural = "Videos"


class ImageMedia(models.Model):
    """
    Model representing an image media.
    """

    IMAGE_TYPE_CHOICES = [(type.name, type.name) for type in ImageType]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    check_sum = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    image_type = models.CharField(max_length=15, choices=IMAGE_TYPE_CHOICES)

    def __str__(self) -> str:
        """
        Return a human-readable string representation of the image media.

        Returns:
            str: A human-readable string representation of the image media.
        """

        return str(self.name)

    class Meta:
        """
        Meta class for the ImageMedia model
        """

        db_table = "image_media"
        verbose_name = "Image Media"
        verbose_name_plural = "Image Medias"


class AudioVideoMedia(models.Model):
    """
    Model representing an audio or video media.
    """

    STATUS_CHOICES = [(status.name, status.name) for status in MediaStatus]
    MEDIA_TYPE_CHOICES = [(type.name, type.name) for type in MediaType]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    check_sum = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    raw_location = models.CharField(max_length=255)
    encoded_location = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)

    def __str__(self) -> str:
        """
        Return a human-readable string representation of the audio or video media.

        Returns:
            str: A human-readable string representation of the audio or video media.
        """

        return str(self.name)

    class Meta:
        """
        Meta class for the AudioVideoMedia model
        """

        db_table = "audio_video_media"
        verbose_name = "Audio Video Media"
        verbose_name_plural = "Audio Video Medias"
