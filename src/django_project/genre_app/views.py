from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)

from src.core._shared.application.use_cases.delete import DeleteRequest
from src.core._shared.application.use_cases.list import ListRequest, ListResponse
from src.core.genre.application.exceptions import (
    GenreNotFound,
    InvalidGenre,
    RelatedCategoriesNotFound,
)
from src.core.genre.application.use_cases.create_genre import CreateGenre
from src.core.genre.application.use_cases.delete_genre import DeleteGenre
from src.core.genre.application.use_cases.list_genre import ListGenre
from src.core.genre.application.use_cases.update_genre import UpdateGenre
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.genre_app.repository import DjangoORMGenreRepository
from src.django_project.genre_app.serializers import (
    CreateGenreRequestSerializer,
    ListGenreResponseSerializer,
    UpdateGenreRequestSerializer,
)
from src.django_project.serializers import (
    CreateResponseSerializer,
    DeleteRequestSerializer,
)


# Create your views here.
class GenreViewSet(viewsets.ViewSet):
    """
    ViewSet for handling genre operations.
    """

    def list(self, request: Request) -> Response:
        """
        Retrieve a list of categories.

        Args:
            request (Request): The request object containing request data.

        Returns:
            Response: A response object containing a list of categories with their
                    id, name, description, and active status.
        """
        order_by = request.query_params.get("order_by", "name")
        reverse_order = request.query_params.get("sort", "asc")
        current_page = request.query_params.get("current_page", 1)

        use_case = ListGenre(DjangoORMGenreRepository())
        res: ListResponse = use_case.execute(
            ListRequest(
                order_by=order_by,
                sort=reverse_order,
                current_page=int(current_page),
            )
        )  # type: ignore

        serializer = ListGenreResponseSerializer(instance=res)

        return Response(
            data=serializer.data,
            status=HTTP_200_OK,
        )

    def create(self, request: Request) -> Response:
        """
        Create a new genre.

        Args:
            request (Request): The request object containing request data.

        Returns:
            Response: A response object containing the created genre data.
        """

        serializer = CreateGenreRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        req = CreateGenre.Input(**serializer.validated_data)  # type: ignore
        use_case = CreateGenre(
            genre_repository=DjangoORMGenreRepository(),
            category_repository=DjangoORMCategoryRepository(),
        )
        try:
            output: CreateGenre.Output = use_case.execute(req)
        except (InvalidGenre, RelatedCategoriesNotFound) as err:
            return Response(
                data={"error": str(err)},
                status=HTTP_400_BAD_REQUEST,
            )

        return Response(
            data=CreateResponseSerializer(instance=output).data,
            status=HTTP_201_CREATED,
        )

    def update(self, request: Request, pk: None) -> Response:
        """
        Update a genre by its id.

        Args:
            request (Request): The request object containing request data.
            pk (uuid.UUID): The id of the genre to be updated.

        Returns:
            Response: A response object containing the updated genre data.
        """

        serializer = UpdateGenreRequestSerializer(
            data={
                **request.data,  # type: ignore
                "id": pk,
            }
        )
        serializer.is_valid(raise_exception=True)

        req = UpdateGenre.Input(**serializer.validated_data)  # type: ignore
        use_case = UpdateGenre(
            genre_repository=DjangoORMGenreRepository(),
            category_repository=DjangoORMCategoryRepository(),
        )

        try:
            use_case.execute(req)
        except GenreNotFound:
            return Response(
                data={"error": "Genre not found"},
                status=HTTP_404_NOT_FOUND,
            )
        except RelatedCategoriesNotFound:
            return Response(
                data={"error": "Related categories not found"},
                status=HTTP_400_BAD_REQUEST,
            )

        return Response(
            status=HTTP_204_NO_CONTENT,
        )

    def destroy(self, request: Request, pk: None) -> Response:
        """
        Delete a genre by its id.

        Args:
            request (Request): The request object containing request data.
            pk (uuid.UUID): The id of the genre to be deleted.

        Returns:
            Response: A response object containing the deleted genre data.
        """

        serializer = DeleteRequestSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)

        req = DeleteRequest(id=pk)  # type: ignore
        use_case = DeleteGenre(DjangoORMGenreRepository())
        try:
            use_case.execute(req)
        except GenreNotFound:
            return Response(
                data={"error": "Genre not found"},
                status=HTTP_404_NOT_FOUND,
            )

        return Response(
            status=HTTP_204_NO_CONTENT,
        )
