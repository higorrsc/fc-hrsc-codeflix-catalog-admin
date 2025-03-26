import uuid
from unittest.mock import create_autospec

import pytest

from src.core._shared.infrastructure.storage.abstract_storage_service import (
    AbstractStorageService,
)
from src.core.video.application.exceptions import VideoNotFound
from src.core.video.application.use_cases.upload_video import UploadVideo
from src.core.video.domain.value_objects import AudioVideoMedia, MediaStatus, Rating
from src.core.video.domain.video import Video
from src.core.video.infra.in_memory_video_repository import InMemoryVideoRepository


class TestUploadVideo:
    """
    Test the UploadVideo use case
    """

    def test_upload_video_media_to_video(self):
        """
        Tests that the UploadVideo use case can upload a video media to a Video
        instance in the repository.

        Given a Video instance with no video media, when the UploadVideo use case
        is executed with the video ID, file name, content, and content type,
        then the video media is uploaded to the storage service and the video
        media is updated in the Video instance in the repository.
        """

        video = Video(
            title="Avatar",
            description="""A paraplegic Marine dispatched to the moon Pandora on a
            unique mission becomes torn between following his orders and protecting
            the world he feels is his home.""",
            duration=162.0,  # type: ignore
            launch_year=2009,
            rating=Rating.AGE_12,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )

        video_repository = InMemoryVideoRepository([video])
        assert video_repository.videos[0] == video

        mock_storage = create_autospec(AbstractStorageService)

        use_case = UploadVideo(
            video_repository,
            mock_storage,
        )
        use_case.execute(
            UploadVideo.Input(
                video_id=video.id,
                file_name="avatar.mp4",
                content=b"avatar_movie_test",
                content_type="video/mp4",
            )
        )

        mock_storage.store.assert_called_once_with(
            file_path=f"videos/{video.id}/avatar.mp4",
            content=b"avatar_movie_test",
            content_type="video/mp4",
        )

        video_from_repository = video_repository.get_by_id(video.id)
        assert video_from_repository.video == AudioVideoMedia(  # type: ignore
            name="avatar.mp4",
            raw_location=f"videos/{video.id}/avatar.mp4",
            encoded_location="",
            status=MediaStatus.PENDING,
        )

    def test_when_video_is_not_found(self):
        """
        When the video to be uploaded is not found in the repository, a
        VideoNotFound exception should be raised with a message indicating
        the video ID.
        """

        video_repository = InMemoryVideoRepository([])
        mock_storage = create_autospec(AbstractStorageService)

        use_case = UploadVideo(
            video_repository,
            mock_storage,
        )
        with pytest.raises(VideoNotFound) as exc_info:
            use_case.execute(
                UploadVideo.Input(
                    video_id=uuid.uuid4(),
                    file_name="avatar.mp4",
                    content=b"avatar_movie_test",
                    content_type="video/mp4",
                )
            )

        assert "Video with ID" in str(exc_info.value)
