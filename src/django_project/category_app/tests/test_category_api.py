import uuid

import pytest
from rest_framework.test import APIClient

from django_project.category_app.repository import DjangoORMCategoryRepository
from src.core.category.domain.category import Category


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
class TestCategoryAPI:
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
        expected_data = [
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
        ]

        response = APIClient().get(url)
        assert response.status_code, 200
        assert response.data, expected_data


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

        assert response.status_code, 400

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
            "id": str(category_movie.id),
            "name": category_movie.name,
            "description": category_movie.description,
            "is_active": category_movie.is_active,
        }

        response = APIClient().get(url)
        assert response.status_code, 200
        assert response.data, expected_data

    def test_return_404_when_category_not_exists(self):
        """
        Test that the API returns 404 when the given ID does not exist.

        When the API is called with GET /api/categories/<id>/ and the given ID does not exist,
        it should return a 404 error.

        The expected result is a 404 status code.
        """

        url = f"/api/categories/{uuid.uuid4()}/"

        response = APIClient().get(url)
        assert response.status_code, 404
