from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from django_project.category_app.repository import DjangoORMCategoryRepository
from src.core.category.application.use_cases.list_category import (
    ListCategory,
    ListCategoryRequest,
)


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

        req = ListCategoryRequest()
        use_case = ListCategory(DjangoORMCategoryRepository())
        res = use_case.execute(req)

        categories = [
            {
                "id": str(category.id),
                "name": category.name,
                "description": category.description,
                "is_active": category.is_active,
            }
            for category in res.data
        ]

        return Response(
            data=categories,
            status=HTTP_200_OK,
        )
