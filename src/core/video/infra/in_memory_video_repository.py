import uuid

from src.core.video.domain.video import Video
from src.core.video.domain.video_repository import VideoRepository


class InMemoryVideoRepository(VideoRepository):
    """
    An in-memory implementation of the VideoRepository interface.
    """

    def __init__(self, videos=None):
        """
        Initialize the in-memory video repository.

        Args:
            videos (list, optional): A list of videos to initialize the repository with.
            Defaults to an empty list if not provided.
        """

        self.videos = videos or []

    def save(self, video: Video):
        """
        Save a video to the in-memory repository.

        Args:
            video (Video): The video to be saved.
        """

        self.videos.append(video)

    def get_by_id(self, video_id: uuid.UUID) -> Video | None:
        """
        Retrieve a video by its ID from the in-memory repository.

        Args:
            id (uuid.UUID): The ID of the video to be retrieved.

        Returns:
            Video: The video with the given ID, or None if it doesn't exist.
        """

        for video in self.videos:
            if video.id == video_id:
                return video

        return None

    def delete(self, video_id: uuid.UUID) -> None:
        """
        Delete a video by its ID from the in-memory repository.

        Args:
            id (uuid.UUID): The ID of the video to be deleted.
        """

        self.videos = [video for video in self.videos if video.id != video_id]

    def update(self, video: Video) -> None:
        """
        Update a video in the in-memory repository.

        Args:
            video (Video): The video to be updated.
        """

        for i, v in enumerate(self.videos):
            if v.id == video.id:
                self.videos[i] = video

    def list(self) -> list[Video]:
        """
        List all videos in the in-memory repository.

        Returns:
            list[Video]: A list of all videos in the repository.
        """

        return list(self.videos)
