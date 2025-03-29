import uuid

from src.core.video.domain.value_objects import Rating
from src.core.video.domain.video import Video
from src.core.video.infra.in_memory_video_repository import InMemoryVideoRepository


class TestSave:
    """
    Test cases for save method of InMemoryVideoRepository.
    """

    def test_can_save_video(self):
        """
        Tests that a Video instance can be saved to the InMemoryVideoRepository.

        This test creates a Video instance and saves it to the repository. It then
        asserts that the video is in the repository and that the repository has
        one video.
        """

        repository = InMemoryVideoRepository()
        video = Video(
            title="Avatar",
            description="""A paraplegic Marine dispatched to the moon Pandora on a
            unique mission becomes torn between following his orders and protecting
            the world he feels is his home.""",
            duration=162.0,  # type: ignore
            launch_year=2009,
            rating=Rating.AGE_12,
            categories={uuid.uuid4(), uuid.uuid4()},
            genres={uuid.uuid4(), uuid.uuid4()},
            cast_members={uuid.uuid4(), uuid.uuid4()},
        )
        repository.save(video)
        assert video in repository.videos
        assert len(repository.videos) == 1


class TestGetById:
    """
    Test cases for get_by_id method of InMemoryVideoRepository.
    """

    def test_can_get_video_by_id(self):
        """
        Tests that a Video instance can be retrieved from the InMemoryVideoRepository
        by its ID.

        This test creates a Video instance and saves it to the repository. It then
        retrieves the video by its ID and asserts that the retrieved video is the
        same as the saved video.
        """

        repository = InMemoryVideoRepository()
        video = Video(
            title="Avatar",
            description="""A paraplegic Marine dispatched to the moon Pandora on a
            unique mission becomes torn between following his orders and protecting
            the world he feels is his home.""",
            duration=162.0,  # type: ignore
            launch_year=2009,
            rating=Rating.AGE_12,
            categories={uuid.uuid4(), uuid.uuid4()},
            genres={uuid.uuid4(), uuid.uuid4()},
            cast_members={uuid.uuid4(), uuid.uuid4()},
        )
        repository.save(video)
        retrieved_video = repository.get_by_id(video.id)
        assert retrieved_video == video

    def test_not_found_video_by_id(self):
        """
        Tests that None is returned when a video is not found in the InMemoryVideoRepository
        by its ID.

        This test creates an InMemoryVideoRepository and asserts that None is returned
        when a video with a non-existent ID is retrieved.
        """

        repository = InMemoryVideoRepository()
        assert repository.get_by_id(uuid.uuid4()) is None


class TestDelete:
    """
    Test cases for delete method of InMemoryVideoRepository.
    """

    def test_can_delete_video(self):
        """
        Tests that a Video instance can be deleted from the InMemoryVideoRepository
        by its ID.

        This test creates a Video instance and saves it to the repository. It then
        deletes the video by its ID and asserts that the video is no longer in the
        repository.
        """

        repository = InMemoryVideoRepository()
        video = Video(
            title="Avatar",
            description="""A paraplegic Marine dispatched to the moon Pandora on a
            unique mission becomes torn between following his orders and protecting
            the world he feels is his home.""",
            duration=162.0,  # type: ignore
            launch_year=2009,
            rating=Rating.AGE_12,
            categories={uuid.uuid4(), uuid.uuid4()},
            genres={uuid.uuid4(), uuid.uuid4()},
            cast_members={uuid.uuid4(), uuid.uuid4()},
        )
        repository.save(video)
        assert video in repository.videos
        repository.delete(video.id)
        assert video not in repository.videos


class TestUpdate:
    """
    Test cases for update method of InMemoryVideoRepository.
    """

    def test_can_update_video(self):
        """
        Tests that a Video instance can be updated in the InMemoryVideoRepository.

        This test creates a Video instance and saves it to the repository. It then
        updates the video and asserts that the video is updated in the repository.
        """

        repository = InMemoryVideoRepository()
        video = Video(
            title="Avatar",
            description="""A paraplegic Marine dispatched to the moon Pandora on a
            unique mission becomes torn between following his orders and protecting
            the world he feels is his home.""",
            duration=162.0,  # type: ignore
            launch_year=2009,
            rating=Rating.AGE_12,
            categories={uuid.uuid4(), uuid.uuid4()},
            genres={uuid.uuid4(), uuid.uuid4()},
            cast_members={uuid.uuid4(), uuid.uuid4()},
        )
        repository.save(video)
        assert video in repository.videos
        video.title = "Avatar: The Way of Water"
        repository.update(video)
        assert video.title == "Avatar: The Way of Water"


class TestList:
    """
    Test cases for list method of InMemoryVideoRepository.
    """

    def test_can_list_videos(self):
        """
        Tests that a list of Video instances can be retrieved from the InMemoryVideoRepository.

        This test creates a Video instance and saves it to the repository. It then
        retrieves the list of videos and asserts that the list contains the saved video.
        """

        repository = InMemoryVideoRepository()
        video = Video(
            title="Avatar",
            description="""A paraplegic Marine dispatched to the moon Pandora on a
            unique mission becomes torn between following his orders and protecting
            the world he feels is his home.""",
            duration=162.0,  # type: ignore
            launch_year=2009,
            rating=Rating.AGE_12,
            categories={uuid.uuid4(), uuid.uuid4()},
            genres={uuid.uuid4(), uuid.uuid4()},
            cast_members={uuid.uuid4(), uuid.uuid4()},
        )
        repository.save(video)

        another_video = Video(
            title="Avatar: The Way of Water",
            description="""Jake Sully lives with his newfound family formed on the
            extrasolar moon Pandora. Once a familiar threat returns to finish what
            was previously started, Jake must work with Neytiri and the army of the
            Na'vi race to protect their home.""",
            duration=162.0,  # type: ignore
            launch_year=2022,
            rating=Rating.AGE_12,
            categories={uuid.uuid4(), uuid.uuid4()},
            genres={uuid.uuid4(), uuid.uuid4()},
            cast_members={uuid.uuid4(), uuid.uuid4()},
        )
        repository.save(another_video)

        videos = repository.list()
        assert video in videos
        assert len(videos) == 2
