import uuid

import pytest
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)
from rest_framework.test import APIClient

from src.config import DEFAULT_PAGE_SIZE
from src.core.category.domain.category import Category
from src.django_project.category_app.repository import DjangoORMCategoryRepository


@pytest.fixture
def category_movie() -> Category:
    """
    Fixture for a Category instance representing movies.

    Returns:
        Category: A Category object with name "Movie" and description "Movies category".
    """

    return Category(
        name="Movie",
        description="Movies category",
    )


@pytest.fixture
def category_tv_show() -> Category:
    """
    Fixture for a Category instance representing TV shows.

    Returns:
        Category: A Category object with name "TV Show" and description "TV Show category".
    """

    return Category(
        name="TV Show",
        description="TV Show category",
    )


@pytest.fixture
def category_repository() -> DjangoORMCategoryRepository:
    """
    Fixture for a DjangoORMCategoryRepository instance.

    Returns:
        DjangoORMCategoryRepository: An instance of the DjangoORMCategoryRepository
        for interacting with the category data in the database.
    """

    return DjangoORMCategoryRepository()


@pytest.mark.django_db
class TestListAPI:
    """
    Test the Category API.
    """

    def test_list_categories(
        self,
        category_movie: Category,
        category_tv_show: Category,
        category_repository: DjangoORMCategoryRepository,
    ):
        """
        Test that the API returns the expected list of categories.

        When the API is called with GET /api/categories/, it should return a list
        of categories with their id, name, description, and is_active status.

        The expected result is a list of two categories with their respective
        information.
        """

        category_repository.save(category_movie)
        category_repository.save(category_tv_show)

        url = "/api/categories/"
        expected_data = {
            "data": [
                {
                    "id": str(category_movie.id),
                    "name": category_movie.name,
                    "description": category_movie.description,
                    "is_active": category_movie.is_active,
                },
                {
                    "id": str(category_tv_show.id),
                    "name": category_tv_show.name,
                    "description": category_tv_show.description,
                    "is_active": category_tv_show.is_active,
                },
            ],
            "meta": {
                "current_page": 1,
                "per_page": DEFAULT_PAGE_SIZE,
                "total": 2,
            },
        }

        response = APIClient().get(url)
        assert response.status_code, 200  # type: ignore
        assert response.data, expected_data  # type: ignore


@pytest.mark.django_db
class TestRetrieveAPI:
    """
    Test the Retrieve API.
    """

    def test_when_id_is_invalid_return_400(self):
        """
        Test that the API returns 400 when the given ID is invalid.

        When the API is called with GET /api/categories/<id>/ and the given ID is invalid,
        it should return a 400 error.

        The expected result is a 400 status code.
        """

        url = "/api/categories/123456789/"
        response = APIClient().get(url)

        assert response.status_code, HTTP_400_BAD_REQUEST  # type: ignore

    def test_return_category_when_exists(
        self,
        category_movie: Category,
        category_tv_show: Category,
        category_repository: DjangoORMCategoryRepository,
    ):
        """
        Test that the API returns the expected category when the given ID exists.

        When the API is called with GET /api/categories/<id>/ and the given ID exists,
        it should return the category with its id, name, description, and is_active status.

        The expected result is the category with its respective information.
        """

        category_repository.save(category_movie)
        category_repository.save(category_tv_show)

        url = f"/api/categories/{category_movie.id}/"
        expected_data = {
            "data": {
                "id": str(category_movie.id),
                "name": category_movie.name,
                "description": category_movie.description,
                "is_active": category_movie.is_active,
            }
        }

        response = APIClient().get(url)
        assert response.status_code, HTTP_200_OK  # type: ignore
        assert response.data, expected_data  # type: ignore

    def test_return_404_when_category_not_exists(self):
        """
        Test that the API returns 404 when the given ID does not exist.

        When the API is called with GET /api/categories/<id>/ and the given ID does not exist,
        it should return a 404 error.

        The expected result is a 404 status code.
        """

        url = f"/api/categories/{uuid.uuid4()}/"

        response = APIClient().get(url)
        assert response.status_code, HTTP_404_NOT_FOUND  # type: ignore


@pytest.mark.django_db
class TestCreateAPI:
    """
    Test the Create API.
    """

    def test_when_data_is_invalid_return_400(self):
        """
        Test that the API returns 400 when the given data is invalid.

        When the API is called with POST /api/categories/ and the given data is invalid,
        it should return a 400 error.

        The expected result is a 400 status code.
        """

        url = "/api/categories/"
        response = APIClient().post(
            path=url,
            data={
                "name": "",
                "description": "Movies category",
            },
            format="json",
        )

        assert response.status_code, HTTP_400_BAD_REQUEST  # type: ignore

    def test_when_data_is_valid_return_201(
        self,
        category_repository: DjangoORMCategoryRepository,
    ):
        """
        Test that the API returns 201 when the given data is valid.

        When the API is called with POST /api/categories/ and the given data is valid,
        it should return a 201 status code.

        The expected result is a 201 status code.
        """

        url = "/api/categories/"
        response = APIClient().post(
            path=url,
            data={
                "name": "Movies",
                "description": "Movies category",
            },
            format="json",
        )

        assert response.status_code, HTTP_201_CREATED  # type: ignore
        created_category_id = uuid.UUID(response.data["id"])  # type: ignore
        assert category_repository.get_by_id(
            category_id=created_category_id
        ) == Category(
            id=created_category_id,
            name="Movies",
            description="Movies category",
            is_active=True,
        )
        assert category_repository.list() == [
            Category(
                id=created_category_id,
                name="Movies",
                description="Movies category",
                is_active=True,
            )
        ]


@pytest.mark.django_db
class TestUpdateAPI:
    """
    Test the Update API.
    """

    def test_when_payload_is_invalid_return_400(self):
        """
        Test that the API returns 400 when the given payload is invalid.

        When the API is called with PUT /api/categories/<id>/ and the given payload is invalid,
        it should return a 400 error.

        The expected result is a 400 status code.
        """

        url = f"/api/categories/1234567890/"
        response = APIClient().put(
            path=url,
            data={
                "name": "",
                "description": "Movies category",
            },
            format="json",
        )

        assert response.status_code, HTTP_400_BAD_REQUEST  # type: ignore
        assert response.data == {  # type: ignore
            "id": ["Must be a valid UUID."],
            "name": ["This field may not be blank."],
            "is_active": ["This field is required."],
        }

    def test_when_payload_is_valid_return_204(
        self,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository,
    ):
        """
        Test that the API returns 204 when the given payload is valid.

        When the API is called with PUT /api/categories/<id>/ and the given payload is valid,
        it should return a 204 status code.

        The expected result is a 204 status code.
        """

        category_repository.save(category_movie)
        url = f"/api/categories/{category_movie.id}/"
        response = APIClient().put(
            path=url,
            data={
                "name": "Movies 2",
                "description": "Movies category updated",
                "is_active": True,
            },
            format="json",
        )

        assert response.status_code, HTTP_204_NO_CONTENT  # type: ignore

        updated_category = category_repository.get_by_id(category_movie.id)
        assert updated_category.name == "Movies 2"  # type: ignore
        assert updated_category.description == "Movies category updated"  # type: ignore
        assert updated_category.is_active is True  # type: ignore

    def test_when_category_not_exists_return_404(self):
        """
        Test that the API returns 404 when the given ID does not exist.

        When the API is called with PUT /api/categories/<id>/ and the given ID does not exist,
        it should return a 404 error.

        The expected result is a 404 status code.
        """

        url = f"/api/categories/{uuid.uuid4()}/"
        response = APIClient().put(
            path=url,
            data={
                "name": "Movies 2",
                "description": "Movies category updated",
                "is_active": True,
            },
            format="json",
        )

        assert response.status_code, HTTP_404_NOT_FOUND  # type: ignore


@pytest.mark.django_db
class TestDeleteAPI:
    """
    Test the Delete API.
    """

    def test_when_id_is_invalid_return_400(self):
        """
        Test that the API returns 400 when the given ID is invalid.

        When the API is called with DELETE /api/categories/<id>/ and the given ID is invalid,
        it should return a 400 error.

        The expected result is a 400 status code.
        """

        url = "/api/categories/1234567890/"
        response = APIClient().delete(url)

        assert response.status_code, HTTP_400_BAD_REQUEST  # type: ignore
        assert response.data == {"id": ["Must be a valid UUID."]}  # type: ignore

    def test_when_category_not_exists_return_404(self):
        """
        Test that the API returns 404 when the given ID does not exist.

        When the API is called with DELETE /api/categories/<id>/ and the given ID does not exist,
        it should return a 404 error.

        The expected result is a 404 status code.
        """

        url = f"/api/categories/{uuid.uuid4()}/"
        response = APIClient().delete(url)

        assert response.status_code, HTTP_404_NOT_FOUND  # type: ignore

    def test_when_category_exists_return_204(
        self,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository,
    ):
        """
        Test that the API returns 204 when the given ID exists.

        When the API is called with DELETE /api/categories/<id>/ and the given ID exists,
        it should return a 204 status code.

        The expected result is a 204 status code.
        """

        category_repository.save(category_movie)
        url = f"/api/categories/{category_movie.id}/"
        response = APIClient().delete(url)

        assert response.status_code, HTTP_204_NO_CONTENT  # type: ignore
        assert category_repository.get_by_id(category_movie.id) is None


@pytest.mark.django_db
class TestPartialUpdateAPI:
    """
    Test the Partial Update API.
    """

    def test_when_payload_is_invalid_return_400(self):
        """
        Test that the API returns 400 when the given payload is invalid.

        When the API is called with PATCH /api/categories/<id>/ and the given payload is invalid,
        it should return a 400 error.

        The expected result is a 400 status code.
        """

        url = "/api/categories/1234567890/"
        response = APIClient().patch(
            path=url,
            data={
                "name": "",
                "description": "Movies category",
            },
            format="json",
        )

        assert response.status_code, HTTP_400_BAD_REQUEST  # type: ignore

    def test_when_category_not_exists_return_404(self):
        """
        Test that the API returns 404 when the given ID does not exist.

        When the API is called with PATCH /api/categories/<id>/ and the given ID does not exist,
        it should return a 404 error.

        The expected result is a 404 status code.
        """

        url = f"/api/categories/{uuid.uuid4()}/"
        response = APIClient().patch(
            path=url,
            data={
                "name": "Movies 2",
                "description": "Movies category updated",
                "is_active": True,
            },
            format="json",
        )

        assert response.status_code, HTTP_404_NOT_FOUND  # type: ignore

    def test_when_category_exists_update_only_name_and_return_204(
        self,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository,
    ):
        """
        Test that the API returns 204 when the given ID exists and the name is updated.

        When the API is called with PATCH /api/categories/<id>/ and the given ID exists,
        it should return a 204 status code and update only the name of the category.

        The expected result is a 204 status code.
        """
        category_repository.save(category_movie)
        url = f"/api/categories/{category_movie.id}/"
        response = APIClient().patch(
            path=url,
            data={
                "name": "Movies 2",
            },
        )

        assert response.status_code, HTTP_204_NO_CONTENT  # type: ignore

        partial_updated_category = category_repository.get_by_id(category_movie.id)
        assert partial_updated_category.name == "Movies 2"  # type: ignore
        assert partial_updated_category.description == category_movie.description  # type: ignore
        assert partial_updated_category.is_active == category_movie.is_active  # type: ignore

    def test_when_category_exists_update_only_description_and_return_204(
        self,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository,
    ):
        """
        Test that the API returns 204 when the given ID exists and the description is updated.

        When the API is called with PATCH /api/categories/<id>/ and the given ID exists,
        it should return a 204 status code and update only the description of the category.

        The expected result is a 204 status code.
        """
        category_repository.save(category_movie)
        url = f"/api/categories/{category_movie.id}/"
        response = APIClient().patch(
            path=url,
            data={
                "description": "Movies category updated",
            },
        )

        assert response.status_code, HTTP_204_NO_CONTENT  # type: ignore

        partial_updated_category = category_repository.get_by_id(category_movie.id)
        assert partial_updated_category.name == category_movie.name  # type: ignore
        assert partial_updated_category.description == "Movies category updated"  # type: ignore
        assert partial_updated_category.is_active == category_movie.is_active  # type: ignore

    def test_when_category_exists_update_only_is_active_and_return_204(
        self,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository,
    ):
        """
        Test that the API returns 204 when the given ID exists and the is_active is updated.

        When the API is called with PATCH /api/categories/<id>/ and the given ID exists,
        it should return a 204 status code and update only the is_active of the category.

        The expected result is a 204 status code.
        """
        category_repository.save(category_movie)
        url = f"/api/categories/{category_movie.id}/"
        response = APIClient().patch(
            path=url,
            data={
                "is_active": False,
            },
        )

        assert response.status_code, HTTP_204_NO_CONTENT  # type: ignore

        partial_updated_category = category_repository.get_by_id(category_movie.id)
        assert partial_updated_category.name == category_movie.name  # type: ignore
        assert partial_updated_category.description == category_movie.description  # type: ignore
        assert partial_updated_category.is_active is False  # type: ignore

    def test_when_category_exists_update_all_fields_and_return_204(
        self,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository,
    ):
        """
        Test that the API returns 204 when the given ID exists and all fields are updated.

        When the API is called with PATCH /api/categories/<id>/ and the given ID exists,
        it should return a 204 status code and update all fields of the category.

        The expected result is a 204 status code.
        """
        category_repository.save(category_movie)
        url = f"/api/categories/{category_movie.id}/"
        response = APIClient().patch(
            path=url,
            data={
                "name": "Movies 2",
                "description": "Movies category updated",
                "is_active": False,
            },
        )

        assert response.status_code, HTTP_204_NO_CONTENT  # type: ignore

        partial_updated_category = category_repository.get_by_id(category_movie.id)
        assert partial_updated_category.name == "Movies 2"  # type: ignore
        assert partial_updated_category.description == "Movies category updated"  # type: ignore
        assert partial_updated_category.is_active is False  # type: ignore
