from src.core._shared.application.use_cases.delete import DeleteRequest, DeleteUseCase
from src.core.video.application.exceptions import VideoNotFound
from src.core.video.domain.video_repository import VideoRepository


class DeleteVideoWithoutMedia(DeleteUseCase):
    """
    Delete a video by its ID.
    """

    def __init__(self, repository: VideoRepository) -> None:
        """
        Initialize the DeleteVideoWithoutMedia use case.

        Args:
            repository (VideoRepository): The video repository.
        """

        super().__init__(
            repository=repository,
            not_found_exception=VideoNotFound,
            not_found_message="Video with id {id} not found",
        )

    def execute(self, request: DeleteRequest) -> None:
        """
        Deletes a video by its ID.

        Args:
            request (DeleteRequest): The request with the ID of the video to be deleted.

        Raises:
            VideoNotFound: If the video is not found.
        """

        super().execute(request)
