from rest_framework.test import APITestCase

from django_project.category_app.repository import DjangoORMCategoryRepository
from src.core.category.domain.category import Category


class TestCategoryAPI(APITestCase):
    """
    Test the Category API.
    """

    def test_list_categories(self):
        """
        Test that the API returns the expected list of categories.

        When the API is called with GET /api/categories/, it should return a list
        of categories with their id, name, description, and is_active status.

        The expected result is a list of two categories with their respective
        information.
        """

        category_movie = Category(
            name="Movie",
            description="Movies category",
        )
        category_tv_show = Category(
            name="TV Show",
            description="TV Show category",
        )

        repository = DjangoORMCategoryRepository()
        repository.save(category_movie)
        repository.save(category_tv_show)

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

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_data)
