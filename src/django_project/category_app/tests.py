from rest_framework.test import APITestCase


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

        url = "/api/categories/"
        expected_data = [
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
        ]
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_data)
