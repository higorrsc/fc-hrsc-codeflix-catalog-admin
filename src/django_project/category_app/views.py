from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK


# Create your views here.
class CategoryViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        """
        Retrieve a list of categories.

        Args:
            request (Request): The request object containing request data.

        Returns:
            Response: A response object containing a list of categories with their
                    id, name, description, and active status.
        """

        return Response(
            data=[
                {
                    "id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
                    "name": "Category 1",
                    "description": "Description 1",
                    "is_active": True,
                },
                {
                    "id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6e",
                    "name": "Category 2",
                    "description": "Description 2",
                    "is_active": True,
                },
            ],            
            status=HTTP_200_OK,
        )
