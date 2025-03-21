from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
)

from src.core._shared.use_cases.list import ListRequest, ListUseCase
from src.core.category.application.exceptions import CategoryNotFound
from src.core.category.application.use_cases.create_category import (
    CreateCategory,
    CreateCategoryRequest,
)
from src.core.category.application.use_cases.delete_category import (
    DeleteCategory,
    DeleteCategoryRequest,
)
from src.core.category.application.use_cases.get_category import (
    GetCategory,
    GetCategoryRequest,
)
from src.core.category.application.use_cases.update_category import (
    UpdateCategory,
    UpdateCategoryRequest,
)
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.category_app.serializers import (
    CreateCategoryRequestSerializer,
    CreateCategoryResponseSerializer,
    DeleteCategoryRequestSerializer,
    ListCategoryResponseSerializer,
    RetrieveCategoryRequestSerializer,
    RetrieveCategoryResponseSerializer,
    UpdateCategoryRequestSerializer,
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

        order_by = request.query_params.get("order_by", "name")
        reverse_order = request.query_params.get("sort", "asc")
        current_page = request.query_params.get("current_page", 1)

        use_case = ListUseCase(DjangoORMCategoryRepository())
        res = use_case.execute(
            ListRequest(
                order_by=order_by,
                sort=reverse_order,
                current_page=int(current_page),
            )
        )

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
            req = GetCategoryRequest(id=serializer.validated_data["id"])  # type: ignore
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

        req = CreateCategoryRequest(**serializer.validated_data)  # type: ignore
        use_case = CreateCategory(DjangoORMCategoryRepository())
        output = use_case.execute(req)

        return Response(
            data=CreateCategoryResponseSerializer(instance=output).data,
            status=HTTP_201_CREATED,
        )

    def update(self, request: Request, pk: None) -> Response:
        """
        Update a category by its id.

        Args:
            request (Request): The request object containing request data.
            pk (uuid.UUID): The id of the category to be updated.

        Returns:
            Response: A response object containing the updated category data.
        """

        serializer = UpdateCategoryRequestSerializer(
            data={
                **request.data,  # type: ignore
                "id": pk,
            }
        )
        serializer.is_valid(raise_exception=True)

        req = UpdateCategoryRequest(**serializer.validated_data)  # type: ignore
        use_case = UpdateCategory(DjangoORMCategoryRepository())

        try:
            use_case.execute(req)
        except CategoryNotFound:
            return Response(
                data={"detail": "Category not found"},
                status=HTTP_404_NOT_FOUND,
            )

        return Response(
            status=HTTP_204_NO_CONTENT,
        )

    def destroy(self, request: Request, pk: None) -> Response:
        """
        Delete a category by its id.

        Args:
            request (Request): The request object containing request data.
            pk (uuid.UUID): The id of the category to be deleted.

        Returns:
            Response: A response object containing the deleted category data.
        """

        serializer = DeleteCategoryRequestSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)

        req = DeleteCategoryRequest(id=pk)  # type: ignore
        use_case = DeleteCategory(DjangoORMCategoryRepository())
        try:
            use_case.execute(req)
        except CategoryNotFound:
            return Response(
                data={"detail": "Category not found"},
                status=HTTP_404_NOT_FOUND,
            )

        return Response(
            status=HTTP_204_NO_CONTENT,
        )

    def partial_update(self, request: Request, pk: None) -> Response:
        """
        Partially update a category by its id.

        Args:
            request (Request): The request object containing request data.
            pk (uuid.UUID): The id of the category to be partially updated.

        Returns:
            Response: A response object containing the partially updated category data.
        """

        serializer = UpdateCategoryRequestSerializer(
            data={
                **request.data,  # type: ignore
                "id": pk,
            },
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        req = UpdateCategoryRequest(**serializer.validated_data)  # type: ignore
        use_case = UpdateCategory(DjangoORMCategoryRepository())

        try:
            use_case.execute(req)
        except CategoryNotFound:
            return Response(
                data={"detail": "Category not found"},
                status=HTTP_404_NOT_FOUND,
            )

        return Response(
            status=HTTP_204_NO_CONTENT,
        )
