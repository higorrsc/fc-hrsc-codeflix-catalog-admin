from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from src.core.genre.application.use_cases.list_genre import ListGenre
from src.django_project.genre_app.repository import DjangoORMGenreRepository
from src.django_project.genre_app.serializers import ListGenreResponseSerializer


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

        use_case = ListGenre(DjangoORMGenreRepository())
        res: ListGenre.Output = use_case.execute(ListGenre.Input())

        serializer = ListGenreResponseSerializer(instance=res)

        return Response(
            data=serializer.data,
            status=HTTP_200_OK,
        )

    # def retrieve(self, request: Request, pk: None) -> Response:
    #     """
    #     Retrieve a genre by its id.

    #     Args:
    #         request (Request): The request object containing request data.
    #         pk (uuid.UUID): The id of the genre to be retrieved.

    #     Returns:
    #         Response: A response object containing the genre data.
    #     """

    #     serializer = RetrieveGenreRequestSerializer(data={"id": pk})
    #     serializer.is_valid(raise_exception=True)

    #     try:
    #         req = GetGenreRequest(id=serializer.validated_data["id"])  # type: ignore
    #         use_case = GetGenre(DjangoORMGenreRepository())
    #         res = use_case.execute(req)
    #     except GenreNotFound:
    #         return Response(
    #             data={"detail": "Genre not found"},
    #             status=HTTP_404_NOT_FOUND,
    #         )

    #     genre_output = RetrieveGenreResponseSerializer(instance=res)

    #     return Response(
    #         data=genre_output.data,
    #         status=HTTP_200_OK,
    #     )

    # def create(self, request: Request) -> Response:
    #     """
    #     Create a new genre.

    #     Args:
    #         request (Request): The request object containing request data.

    #     Returns:
    #         Response: A response object containing the created genre data.
    #     """

    #     serializer = CreateGenreRequestSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)

    #     req = CreateGenreRequest(**serializer.validated_data)  # type: ignore
    #     use_case = CreateGenre(DjangoORMGenreRepository())
    #     output = use_case.execute(req)

    #     return Response(
    #         data=CreateGenreResponseSerializer(instance=output).data,
    #         status=HTTP_201_CREATED,
    #     )

    # def update(self, request: Request, pk: None) -> Response:
    #     """
    #     Update a genre by its id.

    #     Args:
    #         request (Request): The request object containing request data.
    #         pk (uuid.UUID): The id of the genre to be updated.

    #     Returns:
    #         Response: A response object containing the updated genre data.
    #     """

    #     serializer = UpdateGenreRequestSerializer(
    #         data={
    #             **request.data,  # type: ignore
    #             "id": pk,
    #         }
    #     )
    #     serializer.is_valid(raise_exception=True)

    #     req = UpdateGenreRequest(**serializer.validated_data)  # type: ignore
    #     use_case = UpdateGenre(DjangoORMGenreRepository())

    #     try:
    #         use_case.execute(req)
    #     except GenreNotFound:
    #         return Response(
    #             data={"detail": "Genre not found"},
    #             status=HTTP_404_NOT_FOUND,
    #         )

    #     return Response(
    #         status=HTTP_204_NO_CONTENT,
    #     )

    # def destroy(self, request: Request, pk: None) -> Response:
    #     """
    #     Delete a genre by its id.

    #     Args:
    #         request (Request): The request object containing request data.
    #         pk (uuid.UUID): The id of the genre to be deleted.

    #     Returns:
    #         Response: A response object containing the deleted genre data.
    #     """

    #     serializer = DeleteGenreRequestSerializer(data={"id": pk})
    #     serializer.is_valid(raise_exception=True)

    #     req = DeleteGenreRequest(id=pk)  # type: ignore
    #     use_case = DeleteGenre(DjangoORMGenreRepository())
    #     try:
    #         use_case.execute(req)
    #     except GenreNotFound:
    #         return Response(
    #             data={"detail": "Genre not found"},
    #             status=HTTP_404_NOT_FOUND,
    #         )

    #     return Response(
    #         status=HTTP_204_NO_CONTENT,
    #     )

    # def partial_update(self, request: Request, pk: None) -> Response:
    #     """
    #     Partially update a genre by its id.

    #     Args:
    #         request (Request): The request object containing request data.
    #         pk (uuid.UUID): The id of the genre to be partially updated.

    #     Returns:
    #         Response: A response object containing the partially updated genre data.
    #     """

    #     serializer = UpdateGenreRequestSerializer(
    #         data={
    #             **request.data,  # type: ignore
    #             "id": pk,
    #         },
    #         partial=True,
    #     )
    #     serializer.is_valid(raise_exception=True)

    #     req = UpdateGenreRequest(**serializer.validated_data)  # type: ignore
    #     use_case = UpdateGenre(DjangoORMGenreRepository())

    #     try:
    #         use_case.execute(req)
    #     except GenreNotFound:
    #         return Response(
    #             data={"detail": "Genre not found"},
    #             status=HTTP_404_NOT_FOUND,
    #         )

    #     return Response(
    #         status=HTTP_204_NO_CONTENT,
    #     )
