import uuid

from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from django_project.category_app.repository import DjangoORMCategoryRepository
from src.core.category.application.exceptions import CategoryNotFound
from src.core.category.application.use_cases.get_category import (
    GetCategory,
    GetCategoryRequest,
)
from src.core.category.application.use_cases.list_category import (
    ListCategory,
    ListCategoryRequest,
)
from src.core.category.domain.category import Category


# Create your views here.
class CategoryViewSet(viewsets.ViewSet):
    """
    ViewSet for handling category operations.
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

    def retrieve(self, request: Request, pk: None) -> Response:
        """
        Retrieve a category by its id.

        Args:
            request (Request): The request object containing request data.
            pk (uuid.UUID): The id of the category to be retrieved.

        Returns:
            Response: A response object containing the category data.
        """

        try:
            category_id = uuid.UUID(pk)
            req = GetCategoryRequest(category_id)
            use_case = GetCategory(DjangoORMCategoryRepository())
            res = use_case.execute(req)
        except ValueError:
            return Response(
                data={"detail": "Invalid category id"},
                status=HTTP_400_BAD_REQUEST,
            )
        except CategoryNotFound:
            return Response(
                data={"detail": "Category not found"},
                status=HTTP_404_NOT_FOUND,
            )

        return Response(
            data={
                "id": str(res.id),
                "name": res.name,
                "description": res.description,
                "is_active": res.is_active,
            },
            status=HTTP_200_OK,
        )
