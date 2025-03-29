import uuid

import pytest

from src.core.video.domain.events.event import AudioVideoMediaUpdated
from src.core.video.domain.value_objects import (
    AudioVideoMedia,
    ImageMedia,
    MediaStatus,
    MediaType,
    Rating,
)
from src.core.video.domain.video import Video


@pytest.fixture
def video_avatar() -> Video:
    """
    Fixture for a Video instance representing the movie Avatar.

    Returns:
        Video: A Video object with title "Avatar", description of the movie
        plot, duration of 162 minutes, launch year 2009, unpublished status,
        rating for age 12 and above, no categories, four genres,
        and twenty cast members.
    """

    return Video(
        title="Avatar",
        description="""A paraplegic Marine dispatched to the moon Pandora on a
        unique mission becomes torn between following his orders and protecting
        the world he feels is his home.""",
        duration=162.0,  # type: ignore
        launch_year=2009,
        rating=Rating.AGE_12,
        categories=set(uuid.uuid4() for _ in range(0)),
        genres=set(uuid.uuid4() for _ in range(4)),
        cast_members=set(uuid.uuid4() for _ in range(20)),
    )


@pytest.fixture
def new_image_media() -> ImageMedia:
    """
    Fixture for a new ImageMedia instance.

    Returns:
        ImageMedia: An ImageMedia object with a check sum of "1234567890", name
        "new_image_media_name", and location "new/path/to/thumbnail".
    """

    return ImageMedia(
        check_sum="1234567890",
        name="new_image_media_name",
        location="new/path/to/thumbnail",
    )


@pytest.fixture
def new_audio_video_media() -> AudioVideoMedia:
    """
    Fixture for a new AudioVideoMedia instance.

    Returns:
        AudioVideoMedia: An AudioVideoMedia object with a check sum of "1234567890",
        name "new_audio_video_media_name", raw location "new/path/to/raw/file",
        encoded location "new/path/to/encoded/file", and status ERROR.
    """

    return AudioVideoMedia(
        check_sum="1234567890",
        name="new_audio_video_media_name",
        raw_location="new/path/to/raw/file",
        encoded_location="new/path/to/encoded/file",
        status=MediaStatus.ERROR,
        media_type=MediaType.VIDEO,
    )


class TestVideoEntity:
    """
    Test suite for the Video entity.
    """

    def test_valid_video(self, video_avatar: Video) -> None:
        """
        Tests that a Video instance with valid data does not have any validation errors.

        Args:
            video_avatar (Video): A Video instance representing the movie Avatar.
        """

        video_avatar.validate()
        assert video_avatar.notification.has_errors is False

    def test_invalid_video_with_empty_title(self, video_avatar: Video) -> None:
        """
        Tests that a Video instance with an invalid title has a validation error.

        Args:
            video_avatar (Video): A Video instance representing the movie Avatar.
        """

        video_avatar.title = ""
        with pytest.raises(ValueError, match="Title cannot be empty"):
            video_avatar.validate()

    def test_invalid_video_with_long_title(self, video_avatar: Video) -> None:
        """
        Tests that a Video instance with an invalid title has a validation error.

        The title is 256 characters long, which is above the maximum allowed.
        A ValueError is raised with a message indicating that the title must
        have less than 256 characters.

        Args:
            video_avatar (Video): A Video instance representing the movie Avatar.
        """

        video_avatar.title = "A" * 256
        with pytest.raises(
            ValueError,
            match="Title must have less than 256 characters",
        ):
            video_avatar.validate()

    def test_video_with_value_objects(self) -> None:
        """
        Tests that a Video instance with value objects is valid.

        This test creates a Video instance with all value objects and asserts
        that the instance is valid, meaning it has no errors in its notification.
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
            banner=ImageMedia(
                check_sum="123",
                name="banner",
                location="path/to/banner",
            ),
            thumbnail=ImageMedia(
                check_sum="123",
                name="thumbnail",
                location="path/to/thumbnail",
            ),
            thumbnail_half=ImageMedia(
                check_sum="123",
                name="thumbnail_half",
                location="path/to/thumbnail_half",
            ),
            trailer=AudioVideoMedia(
                check_sum="123",
                name="trailer",
                raw_location="path/to/trailer_raw",
                encoded_location="path/to/trailer_encoded",
                status=MediaStatus.PENDING,
                media_type=MediaType.TRAILER,
            ),
        )
        assert video.notification.has_errors is False

    def test_video_update(self, video_avatar: Video) -> None:
        """
        Tests that a Video instance can be updated with new data.

        This test updates the video's title, description, launch year, duration,
        and published status. It then validates the video to ensure that it has
        no errors in its notification.

        Args:
            video_avatar (Video): A Video instance representing the movie Avatar.
        """

        video_avatar.update(
            title="Avatar 2",
            description="""A sequel to the movie Avatar, where Jake Sully returns
            to Pandora to explore the planet's oceans.""",
            launch_year=2022,
            duration=180.0,  # type: ignore
            published=True,
            rating=Rating.AGE_14,
        )
        assert video_avatar.notification.has_errors is False
        assert video_avatar.title == "Avatar 2"
        assert (
            video_avatar.description
            == """A sequel to the movie Avatar, where Jake Sully returns
            to Pandora to explore the planet's oceans."""
        )
        assert video_avatar.launch_year == 2022
        assert video_avatar.duration == 180.0

    def test_add_categories_to_video(self, video_avatar: Video) -> None:
        """
        Tests that a Video instance can add categories.

        This test adds two categories to the video and asserts that the video
        now has two categories.
        """

        categories = set([uuid.uuid4(), uuid.uuid4()])
        video_avatar.add_categories(categories)
        assert len(video_avatar.categories) == 2

    def test_remove_categories_from_video(self, video_avatar: Video) -> None:
        """
        Tests that a Video instance can remove categories.

        This test removes two categories from the video and asserts that the video
        now has zero categories.
        """

        categories = list([uuid.uuid4(), uuid.uuid4()])
        video_avatar.add_categories(set(categories))
        assert len(video_avatar.categories) == 2
        video_avatar.remove_categories(set({categories[0]}))
        assert len(video_avatar.categories) == 1

    def test_add_genres_to_video(self, video_avatar: Video) -> None:
        """
        Tests that a Video instance can add genres.

        This test adds two genres to the video and asserts that the video
        now has two genres.
        """

        genres = set([uuid.uuid4(), uuid.uuid4()])
        video_avatar.add_genres(genres)
        assert len(video_avatar.genres) == 6

    def test_remove_genres_from_video(self, video_avatar: Video) -> None:
        """
        Tests that a Video instance can remove genres.

        This test removes two genres from the video and asserts that the video
        now has zero genres.
        """

        genres = list([uuid.uuid4(), uuid.uuid4()])
        video_avatar.add_genres(set(genres))
        assert len(video_avatar.genres) == 6
        video_avatar.remove_genres(set(genres))
        assert len(video_avatar.genres) == 4

    def test_add_cast_members_to_video(self, video_avatar: Video) -> None:
        """
        Tests that a Video instance can add cast members.

        This test adds two cast members to the video and asserts that the video
        now has two cast members.
        """

        cast_members = set([uuid.uuid4(), uuid.uuid4()])
        video_avatar.add_cast_members(cast_members)
        assert len(video_avatar.cast_members) == 22

    def test_remove_cast_members_from_video(self, video_avatar: Video) -> None:
        """
        Tests that a Video instance can remove cast members.

        This test removes two cast members from the video and asserts that the video
        now has zero cast members.
        """

        cast_members = list([uuid.uuid4(), uuid.uuid4(), uuid.uuid4()])
        video_avatar.add_cast_members(set(cast_members))
        assert len(video_avatar.cast_members) == 23
        video_avatar.remove_cast_members(set({cast_members[0], cast_members[2]}))
        assert len(video_avatar.cast_members) == 21

    def test_update_video_banner(
        self,
        video_avatar: Video,
        new_image_media: ImageMedia,
    ) -> None:
        """
        Tests that a Video instance can update its banner.

        This test updates the video's banner with a new ImageMedia instance and
        asserts that the video's banner has been correctly updated.
        """

        video_avatar.update_banner(new_image_media)
        assert video_avatar.banner == new_image_media
        assert video_avatar.notification.has_errors is False
        assert video_avatar.banner.check_sum == new_image_media.check_sum  # type: ignore
        assert video_avatar.banner.location == new_image_media.location  # type: ignore
        assert video_avatar.banner.name == new_image_media.name  # type: ignore

    def test_update_video_thumbnail(
        self,
        video_avatar: Video,
        new_image_media: ImageMedia,
    ) -> None:
        """
        Tests that a Video instance can update its thumbnail.

        This test updates the video's thumbnail with a new ImageMedia instance and
        asserts that the video's thumbnail has been correctly updated.
        """

        video_avatar.update_thumbnail(new_image_media)
        assert video_avatar.thumbnail == new_image_media
        assert video_avatar.notification.has_errors is False
        assert video_avatar.thumbnail.check_sum == new_image_media.check_sum  # type: ignore
        assert video_avatar.thumbnail.location == new_image_media.location  # type: ignore
        assert video_avatar.thumbnail.name == new_image_media.name  # type: ignore

    def test_update_video_thumbnail_half(
        self,
        video_avatar: Video,
        new_image_media: ImageMedia,
    ) -> None:
        """
        Tests that a Video instance can update its thumbnail half.

        This test updates the video's thumbnail half with a new ImageMedia instance and
        asserts that the video's thumbnail half has been correctly updated.
        """

        video_avatar.update_thumbnail_half(new_image_media)
        assert video_avatar.thumbnail_half == new_image_media
        assert video_avatar.notification.has_errors is False
        assert video_avatar.thumbnail_half.check_sum == new_image_media.check_sum  # type: ignore
        assert video_avatar.thumbnail_half.location == new_image_media.location  # type: ignore
        assert video_avatar.thumbnail_half.name == new_image_media.name  # type: ignore

    def test_update_video_trailer(
        self,
        video_avatar: Video,
        new_audio_video_media: AudioVideoMedia,
    ) -> None:
        """
        Tests that a Video instance can update its trailer.

        This test updates the video's trailer with a new AudioVideoMedia instance and
        asserts that the video's trailer has been correctly updated.
        """

        video_avatar.update_trailer(new_audio_video_media)
        assert video_avatar.trailer == new_audio_video_media
        assert video_avatar.notification.has_errors is False
        assert video_avatar.trailer.check_sum == new_audio_video_media.check_sum  # type: ignore
        assert video_avatar.trailer.raw_location == new_audio_video_media.raw_location  # type: ignore
        assert video_avatar.trailer.encoded_location == new_audio_video_media.encoded_location  # type: ignore
        assert video_avatar.trailer.name == new_audio_video_media.name  # type: ignore
        assert video_avatar.trailer.status == new_audio_video_media.status  # type: ignore
        assert video_avatar.trailer.status == MediaStatus.ERROR  # type: ignore

    def test_update_video_video(
        self,
        video_avatar: Video,
        new_audio_video_media: AudioVideoMedia,
    ) -> None:
        """
        Tests that a Video instance can update its video.

        This test updates the video's video with a new AudioVideoMedia instance and
        asserts that the video's video has been correctly updated.
        """

        video_avatar.update_video(new_audio_video_media)
        assert video_avatar.video == new_audio_video_media
        assert video_avatar.notification.has_errors is False
        assert video_avatar.video.check_sum == new_audio_video_media.check_sum  # type: ignore
        assert video_avatar.video.raw_location == new_audio_video_media.raw_location  # type: ignore
        assert video_avatar.video.encoded_location == new_audio_video_media.encoded_location  # type: ignore
        assert video_avatar.video.name == new_audio_video_media.name  # type: ignore
        assert video_avatar.video.status == new_audio_video_media.status  # type: ignore
        assert video_avatar.video.status == MediaStatus.ERROR  # type: ignore


class TestPublish:
    pass


class TestUpdateVideoMedia:

    def test_update_video_and_dispatch_event(
        self, video_avatar: Video, new_audio_video_media: AudioVideoMedia
    ) -> None:
        video_avatar.update_video(new_audio_video_media)
        assert video_avatar.video == new_audio_video_media

        assert video_avatar.events == [
            AudioVideoMediaUpdated(
                aggregate_id=video_avatar.id,
                file_path=new_audio_video_media.raw_location,
                media_type=MediaType.VIDEO,
            )
        ]
