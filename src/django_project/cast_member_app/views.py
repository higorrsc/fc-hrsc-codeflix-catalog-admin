from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from src.core.cast_member.application.exceptions import InvalidCastMember
from src.core.cast_member.application.use_cases.create_cast_member import (
    CreateCastMember,
)
from src.core.cast_member.application.use_cases.list_cast_member import ListCastMember
from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository
from src.django_project.cast_member_app.serializers import (
    CreateCastMemberRequestSerializer,
    CreateCastMemberResponseSerializer,
    ListCastMemberResponseSerializer,
)


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

        use_case = ListCastMember(DjangoORMCastMemberRepository())
        res: ListCastMember.Output = use_case.execute(ListCastMember.Input())

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

        req: CreateCastMember.Input = CreateCastMember.Input(**serializer.validated_data)  # type: ignore
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

    def update(self, request: Request, pk: None) -> Response: ...
    def destroy(self, request: Request, pk: None) -> Response: ...
