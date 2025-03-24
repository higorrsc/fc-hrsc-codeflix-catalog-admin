import uuid
from abc import ABC, abstractmethod
from typing import List

from src.core.video.domain.video import Video


class VideoRepository(ABC):
    """
    Interface for a genre repository.
    """

    @abstractmethod
    def save(self, video: Video):
        """
        Save a video to the repository.

        Args:
            video (Video): The video to be saved.
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, video_id: uuid.UUID) -> Video | None:
        """
        Retrieve a video by its ID from the repository.

        Args:
            id (uuid.UUID): The ID of the video to be retrieved.

        Returns:
            Video: The video with the given ID, or None if it doesn't exist.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self, video_id: uuid.UUID):
        """
        Delete a video by its ID from the repository.

        Args:
            id (uuid.UUID): The ID of the video to be deleted.
        """
        raise NotImplementedError

    @abstractmethod
    def update(self, video: Video):
        """
        Update a video in the repository.

        Args:
            video (Video): The video to be updated.
        """
        raise NotImplementedError

    @abstractmethod
    def list(self) -> List[Video]:
        """
        List all categories from the repository.

        Returns:
            list[Video]: A list of all categories.
        """
        raise NotImplementedError
