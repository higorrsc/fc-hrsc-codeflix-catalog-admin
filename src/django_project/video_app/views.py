from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from src.core.video.application.exceptions import InvalidVideo, RelatedEntitiesNotFound
from src.core.video.application.use_cases.create_video_without_media import (
    CreateVideoWithoutMedia,
)
from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.genre_app.repository import DjangoORMGenreRepository
from src.django_project.serializers import CreateResponseSerializer
from src.django_project.video_app.repository import DjangoORMVideoRepository
from src.django_project.video_app.serializers import (
    CreateVideoWithoutMediaRequestSerializer,
)


# Create your views here.
class VideoViewSet(viewsets.ViewSet):
    """
    ViewSet for handling video operations.
    """

    def list(self, request: Request) -> Response:
        """
        List all videos.

        Args:
            request (Request): The request object containing request data.

        Returns:
            Response: A response object containing a list of video data.
        """

        raise NotImplementedError

    def retrieve(self, request: Request, pk=None) -> Response:
        """
        Retrieve a video by its id.

        Args:
            request (Request): The request object containing request data.
            pk (uuid.UUID): The id of the video to be retrieved.

        Returns:
            Response: A response object containing the video data.
        """

        raise NotImplementedError

    def create(self, request: Request) -> Response:
        """
        Create a new video without media.

        Args:
            request (Request): The request object containing video data.

        Returns:
            Response: A response object containing the created video data or an error message.

        Raises:
            InvalidVideo: If the video data is invalid.
            RelatedEntitiesNotFound: If any related entities (categories, genres, or cast members)
                are not found.
        """

        serializer = CreateVideoWithoutMediaRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        req = CreateVideoWithoutMedia.Input(**serializer.validated_data)  # type: ignore
        use_case = CreateVideoWithoutMedia(
            DjangoORMVideoRepository(),
            DjangoORMCategoryRepository(),
            DjangoORMGenreRepository(),
            DjangoORMCastMemberRepository(),
        )

        try:
            output: CreateVideoWithoutMedia.Output = use_case.execute(req)
        except (InvalidVideo, RelatedEntitiesNotFound) as err:
            return Response(
                data={"error": str(err)},
                status=HTTP_400_BAD_REQUEST,
            )

        return Response(
            data=CreateResponseSerializer(instance=output).data,
            status=HTTP_201_CREATED,
        )

    def update(self, request: Request, pk=None) -> Response:
        """
        Update a video by its id.

        Args:
            request (Request): The request object containing request data.
            pk (str): The id of the video to be updated.

        Returns:
            Response: A response object containing the updated video data.
        """

        raise NotImplementedError

    def destroy(self, request: Request, pk=None) -> Response:
        """
        Delete a video by its id.

        Args:
            request (Request): The request object containing request data.
            pk (str): The id of the video to be deleted.

        Returns:
            Response: A response object containing the deleted video data.
        """

        raise NotImplementedError

    def partial_update(self, request: Request, pk=None) -> Response:
        """
        Partially update a video by its id.

        Args:
            request (Request): The request object containing request data.
            pk (str): The id of the video to be partially updated.

        Returns:
            Response: A response object containing the partially updated video data.
        """

        raise NotImplementedError
