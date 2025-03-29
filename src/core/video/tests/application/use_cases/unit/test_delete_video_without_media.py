import uuid
from unittest.mock import create_autospec

import pytest

from src.core._shared.application.use_cases.delete import DeleteRequest
from src.core.video.application.exceptions import VideoNotFound
from src.core.video.application.use_cases.delete_video_without_media import (
    DeleteVideoWithoutMedia,
)
from src.core.video.domain.value_objects import Rating
from src.core.video.domain.video import Video
from src.core.video.domain.video_repository import VideoRepository


class TestDeleteVideoWithoutMedia:
    """
    Unit tests for the DeleteVideoWithoutMedia use case.
    """

    def test_delete_video_from_repository(self):
        """
        Tests that a video can be deleted from the VideoRepository using the
        DeleteVideoWithoutMedia use case.

        This test creates a mock Video instance and adds it to the repository. It
        then executes the delete operation by the video's ID and verifies that the
        delete method on the repository is called exactly once with the correct
        video ID.

        Asserts:
            - The repository's delete method is called once with the video's ID.
        """

        video = Video(
            title="Avatar",
            description="""A paraplegic Marine dispatched to the moon Pandora on a
            unique mission becomes torn between following his orders and protecting
            the world he feels is his home.""",
            launch_year=2009,
            duration=162.0,  # type: ignore
            rating=Rating.AGE_12,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )

        mock_video_repository = create_autospec(VideoRepository)
        mock_video_repository.get_by_id.return_value = [video]

        use_case = DeleteVideoWithoutMedia(mock_video_repository)
        use_case.execute(request=DeleteRequest(id=video.id))

        mock_video_repository.delete.assert_called_once_with(video_id=video.id)

    def test_delete_video_not_found(self):
        """
        Tests that the DeleteVideoWithoutMedia use case raises a VideoNotFound
        exception when the video is not found in the repository.

        This test creates a mock VideoRepository that raises a VideoNotFound
        exception when the list method is called. It then executes the delete
        operation by the video's ID and verifies that the VideoNotFound exception
        is raised.

        Asserts:
            - A VideoNotFound exception is raised.
        """

        mock_video_repository = create_autospec(VideoRepository)
        mock_video_repository.get_by_id.return_value = None

        use_case = DeleteVideoWithoutMedia(mock_video_repository)
        with pytest.raises(VideoNotFound) as exc_info:
            use_case.execute(request=DeleteRequest(id=uuid.uuid4()))

        assert "Video with id" in str(exc_info.value)
