from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from src.core.cast_member.application.use_cases.list_cast_member import ListCastMember
from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository
from src.django_project.cast_member_app.serializers import (
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

    def retrieve(self, request: Request, pk: None) -> Response: ...
    def create(self, request: Request) -> Response: ...
    def update(self, request: Request, pk: None) -> Response: ...
    def destroy(self, request: Request, pk: None) -> Response: ...
