import pytest
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
)
from rest_framework.test import APIClient

from src.config import DEFAULT_PAGE_SIZE


@pytest.mark.django_db
class TestCreateAndEditCastMember:
    """
    Test class for testing user can create, edit and delete a cast member
    """

    def test_user_can_create_edit_and_delete_cast_member(self) -> None:
        """
        Verify that a user can create, edit and delete a cast member, and that the edited
        cast member data is correct.

        This test creates a cast member, verifies that it was created, updates the cast
        member, verifies that it was updated, deletes the cast member, and verifies that it
        was deleted.
        """

        api_client = APIClient()

        list_response = api_client.get("/api/cast_members/")
        assert list_response.status_code == HTTP_200_OK  # type: ignore

        create_response = api_client.post(
            path="/api/cast_members/",
            data={"name": "Robert Downey Jr.", "type": "ACTOR"},
            format="json",
        )
        assert create_response.status_code == HTTP_201_CREATED  # type: ignore
        cast_member_response_id = create_response.data["id"]  # type: ignore

        list_response = api_client.get("/api/cast_members/")
        assert list_response.status_code == HTTP_200_OK  # type: ignore
        assert len(list_response.data["data"]) == 1  # type: ignore
        assert list_response.data == {  # type: ignore
            "data": [
                {
                    "id": cast_member_response_id,
                    "name": "Robert Downey Jr.",
                    "type": "ACTOR",
                }
            ],
            "meta": {
                "current_page": 1,
                "per_page": DEFAULT_PAGE_SIZE,
                "total": 1,
            },
        }

        update_response = api_client.put(
            path=f"/api/cast_members/{cast_member_response_id}/",
            data={
                "name": "Cristian Bale",
                "type": "ACTOR",
            },
            format="json",
        )
        assert update_response.status_code == HTTP_204_NO_CONTENT  # type: ignore

        delete_response = api_client.delete(
            f"/api/cast_members/{cast_member_response_id}/"
        )
        assert delete_response.status_code == HTTP_204_NO_CONTENT  # type: ignore

        list_response = api_client.get("/api/cast_members/")
        assert list_response.status_code == HTTP_200_OK  # type: ignore

        update_response = api_client.put(
            path=f"/api/cast_members/{cast_member_response_id}/",
            data={
                "name": "Cristian Bale",
                "type": "ACTOR",
            },
            format="json",
        )
        assert update_response.status_code == HTTP_404_NOT_FOUND  # type: ignore

        delete_response = api_client.delete(
            f"/api/cast_members/{cast_member_response_id}/"
        )
        assert delete_response.status_code == HTTP_404_NOT_FOUND  # type: ignore
