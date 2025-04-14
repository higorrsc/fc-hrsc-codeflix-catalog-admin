import pytest
from rest_framework.test import APIClient

from src.config import DEFAULT_PAGE_SIZE


@pytest.mark.django_db
class TestCreateAndEditCategory:
    """
    Test class for testing user can create and edit a category
    """

    def test_user_can_create_and_edit_category(
        self,
        api_client_with_auth: APIClient,
    ) -> None:
        """
        Verify that a user can create and edit a category, and that the edited
        category data is correct.

        This test creates a category, verifies that it was created, updates the
        category, verifies that it was updated, deletes the category, and verifies
        that it was deleted.
        """

        # Verify that list categories is empty
        list_response = api_client_with_auth.get("/api/categories/")
        assert list_response.status_code == 200  # type: ignore

        # Create category
        create_response = api_client_with_auth.post(
            "/api/categories/",
            data={"name": "Test Category", "description": "Test Category Description"},
            format="json",
        )
        assert create_response.status_code == 201  # type: ignore
        category_response_id = create_response.data["id"]  # type: ignore

        # Verify that category was created
        list_response = api_client_with_auth.get("/api/categories/")
        assert list_response.status_code == 200  # type: ignore
        assert len(list_response.data["data"]) == 1  # type: ignore
        assert list_response.data == {  # type: ignore
            "data": [
                {
                    "id": category_response_id,
                    "name": "Test Category",
                    "description": "Test Category Description",
                    "is_active": True,
                }
            ],
            "meta": {
                "current_page": 1,
                "per_page": DEFAULT_PAGE_SIZE,
                "total": 1,
            },
        }

        # Verify that category is active
        get_response = api_client_with_auth.get(
            f"/api/categories/{category_response_id}/"
        )
        assert get_response.status_code == 200  # type: ignore
        assert get_response.data == {  # type: ignore
            "data": {
                "id": category_response_id,
                "name": "Test Category",
                "description": "Test Category Description",
                "is_active": True,
            }
        }

        # Update category
        update_response = api_client_with_auth.put(
            f"/api/categories/{category_response_id}/",
            data={
                "name": "Test Category Updated",
                "description": "Test Category Description Updated",
                "is_active": False,
            },
            format="json",
        )
        assert update_response.status_code == 204  # type: ignore

        # Verify that category was updated
        list_response = api_client_with_auth.get("/api/categories/")
        assert list_response.status_code == 200  # type: ignore
        assert len(list_response.data["data"]) == 1  # type: ignore
        assert list_response.data == {  # type: ignore
            "data": [
                {
                    "id": category_response_id,
                    "name": "Test Category Updated",
                    "description": "Test Category Description Updated",
                    "is_active": False,
                }
            ],
            "meta": {
                "current_page": 1,
                "per_page": DEFAULT_PAGE_SIZE,
                "total": 1,
            },
        }

        # Delete category
        delete_response = api_client_with_auth.delete(
            f"/api/categories/{category_response_id}/"
        )
        assert delete_response.status_code == 204  # type: ignore

        # Verify that category was deleted
        list_response = api_client_with_auth.get("/api/categories/")
        assert list_response.status_code == 200  # type: ignore
        assert len(list_response.data["data"]) == 0  # type: ignore
