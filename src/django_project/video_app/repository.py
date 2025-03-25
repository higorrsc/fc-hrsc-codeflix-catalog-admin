import uuid
from typing import List

from django.db import transaction

from src.core.video.domain.video import Video
from src.core.video.domain.video_repository import VideoRepository
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

        try:
            self.video_model.objects.filter(pk=video_id).delete()
        except self.video_model.DoesNotExist:
            return None

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
            video_model.id = video.id
            video_model.title = video.title
            video_model.description = video.description
            video_model.launch_year = video.launch_year
            video_model.duration = video.duration
            video_model.published = video.published
            video_model.rating = video.rating  # type: ignore
            video_model.save()
            video_model.categories.set(video.categories)
            video_model.genres.set(video.genres)
            video_model.cast_members.set(video.cast_members)

    def list(self) -> List[Video]:
        """
        Retrieve a list of all videos from the repository.

        Returns:
            List[Video]: A list of Video instances representing all videos in the repository.
        """

        return [
            VideoModelMapper.to_entity(video_model)
            for video_model in self.video_model.objects.all()
            # Video(
            #     id=video.id,
            #     title=video.title,
            #     description=video.description,
            #     launch_year=video.launch_year,
            #     duration=video.duration,
            #     published=video.published,
            #     rating=video.rating,  # type: ignore
            #     categories={category.id for category in video.categories.all()},
            #     genres={genre.id for genre in video.genres.all()},
            #     cast_members={
            #         cast_member.id for cast_member in video.cast_members.all()
            #     },
            # )
            # for video in VideoModel.objects.all()
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
            published=video_model.published,
            rating=video_model.rating,  # type: ignore
            categories={category.id for category in video_model.categories.all()},
            genres={genre.id for genre in video_model.genres.all()},
            cast_members={
                cast_member.id for cast_member in video_model.cast_members.all()
            },
        )
