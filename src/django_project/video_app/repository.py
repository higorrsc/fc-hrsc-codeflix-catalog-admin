import uuid
from typing import List

from django.db import transaction

from src.core.video.domain.value_objects import (
    AudioVideoMedia,
    ImageMedia,
    ImageType,
    MediaStatus,
    MediaType,
)
from src.core.video.domain.video import Video
from src.core.video.domain.video_repository import VideoRepository
from src.django_project.video_app.models import AudioVideoMedia as AudioVideoMediaModel
from src.django_project.video_app.models import ImageMedia as ImageMediaModel
from src.django_project.video_app.models import Video as VideoModel


class DjangoORMVideoRepository(VideoRepository):
    """
    Django ORM implementation for a video repository.
    """

    def __init__(self, video_model: VideoModel | None = None):
        """
        Initialize the DjangoORMVideoRepository with an optional VideoModel.

        Args:
            video_model (VideoModel | None): An optional VideoModel instance.
                If not provided, the default VideoModel is used.
        """

        self.video_model = video_model or VideoModel

    def save(self, video: Video):
        """
        Save a video to the repository.

        Args:
            video (Video): The video to be saved.
        """

        with transaction.atomic():
            video_model = self.video_model.objects.create(
                id=video.id,
                title=video.title,
                description=video.description,
                published=video.published,
                launch_year=video.launch_year,
                duration=video.duration,
                rating=video.rating,
            )
            video_model.categories.set(video.categories)
            video_model.genres.set(video.genres)
            video_model.cast_members.set(video.cast_members)

    def get_by_id(self, video_id: uuid.UUID) -> Video | None:
        """
        Retrieve a video by its ID from the repository.

        Args:
            id (uuid.UUID): The ID of the video to be retrieved.

        Returns:
            Video: The video with the given ID, or None if it doesn't exist.
        """

        try:
            video_model = self.video_model.objects.get(pk=video_id)
        except self.video_model.DoesNotExist:
            return None

        return VideoModelMapper.to_entity(video_model)

    def delete(self, video_id: uuid.UUID) -> None:
        """
        Delete a video by its ID from the repository.

        Args:
            id (uuid.UUID): The ID of the video to be deleted.
        """

        self.video_model.objects.filter(pk=video_id).delete()

    def update(self, video: Video) -> None:
        """
        Update a video in the repository.

        Args:
            video (Video): The video to be updated.
        """

        try:
            video_model = self.video_model.objects.get(pk=video.id)
        except self.video_model.DoesNotExist:
            return None

        with transaction.atomic():
            AudioVideoMediaModel.objects.filter(id=video_model.id).delete()
            video_model.title = video.title
            video_model.description = video.description
            video_model.launch_year = video.launch_year
            video_model.duration = video.duration
            video_model.published = video.published
            video_model.rating = video.rating  # type: ignore
            video_model.categories.set(video.categories)
            video_model.genres.set(video.genres)
            video_model.cast_members.set(video.cast_members)
            if video.video:
                video_model.video = AudioVideoMediaMapper.to_model(video.video)  # type: ignore
                video_model.video.save()  # type: ignore
            # video_model.video = (
            #     AudioVideoMediaModel.objects.create(  # type: ignore
            #         name=video.video.name,  # type: ignore
            #         raw_location=video.video.raw_location,  # type: ignore
            #         encoded_location=video.video.encoded_location,  # type: ignore
            #         check_sum=video.video.check_sum,  # type: ignore
            #         status=video.video.status,  # type: ignore
            #     )
            #     if video.video
            #     else None
            # )
            video_model.save()
        return None

    def list(self) -> List[Video]:
        """
        Retrieve a list of all videos from the repository.

        Returns:
            List[Video]: A list of Video instances representing all videos in the repository.
        """

        return [
            VideoModelMapper.to_entity(video_model)
            for video_model in self.video_model.objects.all()
        ]


class VideoModelMapper:
    """
    A class for mapping between Video and VideoModel.
    """

    @staticmethod
    def to_model(video: Video) -> VideoModel:
        """
        Maps a Video entity to a VideoModel.

        Args:
            video (Video): The video entity to be mapped.

        Returns:
            VideoModel: The mapped VideoModel.
        """

        return VideoModel(
            id=video.id,
            title=video.title,
            description=video.description,
            launch_year=video.launch_year,
            duration=video.duration,
            published=video.published,
            rating=video.rating,
        )

    @staticmethod
    def to_entity(video_model: VideoModel) -> Video:
        """
        Maps a VideoModel to a Video entity.

        Args:
            video_model (VideoModel): The video model to be mapped.

        Returns:
            Video: The mapped Video entity.
        """

        return Video(
            id=video_model.id,
            title=video_model.title,
            description=video_model.description,
            launch_year=video_model.launch_year,
            duration=video_model.duration,
            rating=video_model.rating,  # type: ignore
            published=video_model.published,
            categories={category.id for category in video_model.categories.all()},
            genres={genre.id for genre in video_model.genres.all()},
            cast_members={
                cast_member.id for cast_member in video_model.cast_members.all()
            },
            banner=ImageMediaMapper.to_entity(
                video_model.banner if video_model.banner else None  # type: ignore
            ),
            thumbnail=ImageMediaMapper.to_entity(
                video_model.thumbnail if video_model.thumbnail else None  # type: ignore
            ),
            thumbnail_half=ImageMediaMapper.to_entity(
                video_model.thumbnail_half if video_model.thumbnail_half else None  # type: ignore
            ),
            trailer=AudioVideoMediaMapper.to_entity(
                video_model.trailer if video_model.trailer else None  # type: ignore
            ),
            video=AudioVideoMediaMapper.to_entity(
                video_model.video if video_model.video else None  # type: ignore
            ),
        )


class AudioVideoMediaMapper:
    """
    A class for mapping between AudioVideoMedia and AudioVideoMediaModel.
    """

    @staticmethod
    def to_entity(
        audio_video_media_model: AudioVideoMediaModel,
    ) -> AudioVideoMedia | None:
        """
        Maps an AudioVideoMediaModel to an AudioVideoMedia entity.

        Args:
            audio_video_media_model (AudioVideoMediaModel): The model to be mapped.

        Returns:
            AudioVideoMedia | None: The mapped AudioVideoMedia entity, or None if the model is None.
        """

        if not audio_video_media_model:
            return None

        return AudioVideoMedia(
            name=audio_video_media_model.name,
            raw_location=audio_video_media_model.raw_location,
            encoded_location=audio_video_media_model.encoded_location,
            check_sum=audio_video_media_model.check_sum,
            status=MediaStatus(audio_video_media_model.status),
            media_type=MediaType(audio_video_media_model.media_type),
        )

    @staticmethod
    def to_model(audio_video_media: AudioVideoMedia) -> AudioVideoMediaModel | None:
        """
        Maps an AudioVideoMedia entity to an AudioVideoMediaModel.

        Args:
            audio_video_media (AudioVideoMedia): The entity to be mapped.

        Returns:
            AudioVideoMediaModel | None: The mapped AudioVideoMediaModel, or None if
                                         the entity is None.
        """
        if not audio_video_media:
            return None

        return AudioVideoMediaModel(
            name=audio_video_media.name,
            raw_location=audio_video_media.raw_location,
            encoded_location=audio_video_media.encoded_location,
            check_sum=audio_video_media.check_sum,
            status=audio_video_media.status,
            media_type=audio_video_media.media_type,
        )


class ImageMediaMapper:
    """
    A class for mapping between ImageMedia and ImageMediaModel.
    """

    @staticmethod
    def to_entity(image_media_model: ImageMediaModel) -> ImageMedia | None:
        """
        Maps an ImageMediaModel to an ImageMedia entity.

        Args:
            image_media_model (ImageMediaModel): The model to be mapped.

        Returns:
            ImageMedia | None: The mapped ImageMedia entity, or None if the model is None.
        """

        if not image_media_model:
            return None

        return ImageMedia(
            name=image_media_model.name,
            location=image_media_model.location,
            image_type=ImageType(image_media_model.image_type),
            check_sum=image_media_model.check_sum,
        )

    @staticmethod
    def to_model(image_media: ImageMedia) -> ImageMediaModel | None:
        """
        Maps an ImageMedia entity to an ImageMediaModel.

        Args:
            image_media (ImageMedia): The entity to be mapped.

        Returns:
            ImageMediaModel | None: The mapped ImageMediaModel, or None if the entity is None.
        """

        if not image_media:
            return None

        return ImageMediaModel(
            name=image_media.name,
            location=image_media.location,
            image_type=image_media.image_type,
            check_sum=image_media.check_sum,
        )
