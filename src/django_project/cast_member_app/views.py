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
from src.core.cast_member.application.exceptions import (
    CastMemberNotFound,
    InvalidCastMember,
)
from src.core.cast_member.application.use_cases.create_cast_member import (
    CreateCastMember,
)
from src.core.cast_member.application.use_cases.delete_cast_member import (
    DeleteCastMember,
)
from src.core.cast_member.application.use_cases.list_cast_member import ListCastMember
from src.core.cast_member.application.use_cases.update_cast_member import (
    UpdateCastMember,
)
from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository
from src.django_project.cast_member_app.serializers import (
    CreateCastMemberRequestSerializer,
    CreateCastMemberResponseSerializer,
    ListCastMemberResponseSerializer,
    UpdateCastMemberRequestSerializer,
)
from src.django_project.serializers import DeleteRequestSerializer


class CastMemberViewSet(viewsets.ViewSet):
    """
    CastMember ViewSet
    """

    def list(self, request: Request) -> Response:
        """
        List all cast members.

        Returns:
            Response: A response containing a list of CastMemberOutput objects.
        """

        order_by = request.query_params.get("order_by", "name")
        reverse_order = request.query_params.get("sort", "asc")
        current_page = request.query_params.get("current_page", 1)

        use_case = ListCastMember(DjangoORMCastMemberRepository())
        res: ListResponse = use_case.execute(
            ListRequest(
                order_by=order_by,
                sort=reverse_order,
                current_page=int(current_page),
            )
        )

        serializer = ListCastMemberResponseSerializer(instance=res)

        return Response(
            data=serializer.data,
            status=HTTP_200_OK,
        )

    def create(self, request: Request) -> Response:
        """
        Create a new cast member.

        Args:
            request (Request): The request object containing request data.

        Returns:
            Response: A response object containing the created cast member data.
        """

        serializer = CreateCastMemberRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        req: CreateCastMember.Input = CreateCastMember.Input(
            **serializer.validated_data,  # type: ignore
        )
        use_case = CreateCastMember(DjangoORMCastMemberRepository())
        try:
            output: CreateCastMember.Output = use_case.execute(req)
        except InvalidCastMember as e:
            return Response(
                data={"error": str(e)},
                status=HTTP_400_BAD_REQUEST,
            )

        return Response(
            data=CreateCastMemberResponseSerializer(instance=output).data,
            status=HTTP_201_CREATED,
        )

    def update(self, request: Request, pk: None) -> Response:
        """
        Update a cast member by its id.

        Args:
            request (Request): The request object containing request data.
            pk (uuid.UUID): The id of the cast member to be updated.

        Returns:
            Response: A response object containing the updated cast member data.
        """

        serializer = UpdateCastMemberRequestSerializer(
            data={
                **request.data,  # type: ignore
                "id": pk,
            }
        )
        serializer.is_valid(raise_exception=True)

        req: UpdateCastMember.Input = UpdateCastMember.Input(
            **serializer.validated_data,  # type: ignore
        )
        use_case = UpdateCastMember(DjangoORMCastMemberRepository())
        try:
            use_case.execute(req)
        except InvalidCastMember as e:
            return Response(
                data={"error": str(e)},
                status=HTTP_400_BAD_REQUEST,
            )
        except CastMemberNotFound:
            return Response(
                data={"detail": "Cast member not found"},
                status=HTTP_404_NOT_FOUND,
            )

        return Response(
            status=HTTP_204_NO_CONTENT,
        )

    def destroy(self, request: Request, pk: None) -> Response:
        """
        Delete a cast member by its id.

        Args:
            request (Request): The request object containing request data.
            pk (uuid.UUID): The id of the cast member to be deleted.

        Returns:
            Response: A response object containing the deleted cast member data.
        """

        serializer = DeleteRequestSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)

        req = DeleteRequest(**serializer.validated_data)  # type: ignore

        use_case = DeleteCastMember(DjangoORMCastMemberRepository())
        try:
            use_case.execute(req)
        except CastMemberNotFound:
            return Response(
                data={"detail": "Cast member not found"},
                status=HTTP_404_NOT_FOUND,
            )

        return Response(
            status=HTTP_204_NO_CONTENT,
        )
