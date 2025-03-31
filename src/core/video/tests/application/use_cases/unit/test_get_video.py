import uuid
from unittest.mock import create_autospec

import pytest

from src.core.video.application.exceptions import VideoNotFound
from src.core.video.application.use_cases.get_video import GetVideo
from src.core.video.domain.value_objects import (
    AudioVideoMedia,
    ImageMedia,
    ImageType,
    MediaStatus,
    MediaType,
    Rating,
)
from src.core.video.domain.video import Video
from src.core.video.domain.video_repository import VideoRepository


class TestGetVideo:
    """
    Test class for the GetVideo use case
    """

    def test_get_video_with_valid_id(self) -> None:
        """
        When getting a video by its ID, it returns a VideoOutput with the data of
        the video.

        This test verifies that the `get_video` use case returns a VideoOutput with
        the data of the video when given a valid ID.
        """

        avatar_video = Video(
            title="Avatar",
            description="A paraplegic Marine dispatched to the moon Pandora...",
            duration=162.0,  # type: ignore
            launch_year=2009,
            rating=Rating.AGE_12,
            categories={uuid.uuid4()},
            genres={uuid.uuid4()},
            cast_members={uuid.uuid4(), uuid.uuid4()},
            banner=ImageMedia(
                name="banner",
                location="location",
                image_type=ImageType.BANNER,
                check_sum="123",
            ),
            thumbnail=ImageMedia(
                name="thumbnail",
                location="location",
                image_type=ImageType.THUMBNAIL,
                check_sum="123",
            ),
            thumbnail_half=ImageMedia(
                name="thumbnail_half",
                location="location",
                image_type=ImageType.THUMBNAIL_HALF,
                check_sum="123",
            ),
            trailer=AudioVideoMedia(
                name="trailer",
                raw_location="location",
                encoded_location="location",
                status=MediaStatus.PENDING,
                media_type=MediaType.TRAILER,
                check_sum="123",
            ),
            video=AudioVideoMedia(
                name="video",
                raw_location="location",
                encoded_location="location",
                status=MediaStatus.PENDING,
                media_type=MediaType.VIDEO,
                check_sum="123",
            ),
        )

        repository = create_autospec(VideoRepository)
        repository.get_by_id.return_value = avatar_video

        use_case = GetVideo(repository=repository)
        result: GetVideo.Output = use_case.execute(GetVideo.Input(avatar_video.id))  # type: ignore

        assert result.id == avatar_video.id
        assert result.title == avatar_video.title
        assert result.description == avatar_video.description
        assert result.launch_year == avatar_video.launch_year
        assert result.duration == avatar_video.duration
        assert result.rating == avatar_video.rating
        assert result.published == avatar_video.published
        assert result.categories == avatar_video.categories
        assert result.genres == avatar_video.genres
        assert result.cast_members == avatar_video.cast_members
        assert result.banner == avatar_video.banner
        assert result.thumbnail == avatar_video.thumbnail
        assert result.thumbnail_half == avatar_video.thumbnail_half
        assert result.trailer == avatar_video.trailer
        assert result.video == avatar_video.video

    def test_get_video_with_invalid_id(self) -> None:
        """
        When getting a video by an invalid ID, it raises a VideoNotFound exception.

        This test verifies that the `get_video` use case raises a VideoNotFound
        exception when given an invalid ID.
        """

        repository = create_autospec(VideoRepository)
        repository.get_by_id.return_value = None

        use_case = GetVideo(repository=repository)
        invalid_id = uuid.uuid4()

        with pytest.raises(VideoNotFound) as exc_info:
            use_case.execute(GetVideo.Input(invalid_id))

        repository.get_by_id.assert_called_once_with(invalid_id)
        assert str(exc_info.value) == f"Video with id {invalid_id} not found"
