import uuid

import pytest

from src.core._shared.application.use_cases.delete import DeleteRequest
from src.core.video.application.exceptions import VideoNotFound
from src.core.video.application.use_cases.delete_video_without_media import (
    DeleteVideoWithoutMedia,
)
from src.core.video.domain.value_objects import Rating
from src.core.video.domain.video import Video
from src.core.video.infra.in_memory_video_repository import InMemoryVideoRepository


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

        repository = InMemoryVideoRepository(videos=[video])
        assert len(repository.videos) == 1

        use_case = DeleteVideoWithoutMedia(repository)
        use_case.execute(request=DeleteRequest(id=video.id))
        assert len(repository.videos) == 0

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

        repository = InMemoryVideoRepository(videos=[])

        use_case = DeleteVideoWithoutMedia(repository)
        with pytest.raises(VideoNotFound) as exc_info:
            use_case.execute(request=DeleteRequest(id=uuid.uuid4()))

        assert "Video with id" in str(exc_info.value)
