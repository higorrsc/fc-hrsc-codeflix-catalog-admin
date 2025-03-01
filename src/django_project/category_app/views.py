import uuid

from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND

from django_project.category_app.repository import DjangoORMCategoryRepository
from django_project.category_app.serializers import (
    CategoryResponseSerializer,
    CreateCategoryRequestSerializer,
    CreateCategoryResponseSerializer,
    ListCategoryResponseSerializer,
    RetrieveCategoryRequestSerializer,
    RetrieveCategoryResponseSerializer,
)
from src.core.category.application.exceptions import CategoryNotFound
from src.core.category.application.use_cases.create_category import (
    CreateCategory,
    CreateCategoryRequest,
)
from src.core.category.application.use_cases.get_category import (
    GetCategory,
    GetCategoryRequest,
)
from src.core.category.application.use_cases.list_category import (
    ListCategory,
    ListCategoryRequest,
)


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

        serializer = ListCategoryResponseSerializer(instance=res)

        return Response(
            data=serializer.data,
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

        serializer = RetrieveCategoryRequestSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)

        try:
            req = GetCategoryRequest(id=serializer.validated_data["id"])
            use_case = GetCategory(DjangoORMCategoryRepository())
            res = use_case.execute(req)
        except CategoryNotFound:
            return Response(
                data={"detail": "Category not found"},
                status=HTTP_404_NOT_FOUND,
            )

        category_output = RetrieveCategoryResponseSerializer(instance=res)

        return Response(
            data=category_output.data,
            status=HTTP_200_OK,
        )

    def create(self, request: Request) -> Response:
        """
        Create a new category.

        Args:
            request (Request): The request object containing request data.

        Returns:
            Response: A response object containing the created category data.
        """

        serializer = CreateCategoryRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        input = CreateCategoryRequest(**serializer.validated_data)
        use_case = CreateCategory(DjangoORMCategoryRepository())
        output = use_case.execute(input)

        return Response(
            data=CreateCategoryResponseSerializer(instance=output).data,
            status=HTTP_201_CREATED,
        )
