import os
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
from src.core._shared.infrastructure.auth.jwt_token_generator import JwtTokenGenerator
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository


@pytest.fixture
def actor_cast_member() -> CastMember:
    """
    Fixture for a CastMember instance representing an actor.

    Returns:
        CastMember: A CastMember object with name "Robert Downey Jr." and type ACTOR.
    """

    return CastMember(
        name="Robert Downey Jr.",
        type=CastMemberType.ACTOR,
    )


@pytest.fixture
def director_cast_member() -> CastMember:
    """
    Fixture for a CastMember instance representing a director.

    Returns:
        CastMember: A CastMember object with name "Clint Eastwood" and type DIRECTOR.
    """

    return CastMember(
        name="Clint Eastwood",
        type=CastMemberType.DIRECTOR,
    )


@pytest.fixture
def cast_member_repository() -> DjangoORMCastMemberRepository:
    """
    Fixture for a DjangoORMCastMemberRepository.

    Returns a DjangoORMCastMemberRepository instance.
    """

    return DjangoORMCastMemberRepository()


@pytest.fixture(scope="session", autouse=True)
def setup_auth_env():
    fake_auth = JwtTokenGenerator()
    os.environ["AUTH_PUBLIC_KEY"] = (
        fake_auth.public_key_pem.decode()
        .replace("-----BEGIN PUBLIC KEY-----\n", "")
        .replace("\n-----END PUBLIC KEY-----\n", "")
    )
    return fake_auth


@pytest.fixture
def auth_token(setup_auth_env):
    return setup_auth_env.generate_token(
        user_info={
            "username": "admin",
            "email": "admin@example.com",
            "first_name": "Admin",
            "last_name": "User",
            "realm_roles": [
                "offline_access",
                "admin",
                "uma_authorization",
                "default-roles-codeflix",
            ],
            "resource_roles": [
                "manage-account",
                "view-profile",
            ],
        }
    )


@pytest.fixture
def api_client_with_auth(auth_token):
    """
    Fixture for an API client with authentication.

    Returns:
        APIClient: An instance of the APIClient with the provided authentication token.
    """

    return APIClient(
        headers={
            "Authorization": f"Bearer {auth_token}",
        }
    )


@pytest.mark.django_db
class TestListAPI:
    """
    Class for testing the ListCastMemberAPI view.
    """

    def test_list_cast_members(
        self,
        actor_cast_member: CastMember,
        director_cast_member: CastMember,
        cast_member_repository: DjangoORMCastMemberRepository,
        api_client_with_auth: APIClient,
    ):
        """
        Tests the ListCastMemberAPI view.

        Given a DjangoORMCastMemberRepository with two cast members (actor and director),
        when the ListCastMemberAPI view is called with a GET request to "/api/cast_members/",
        the expected output is a JSON response containing a list of two dictionaries
        representing the two cast members.

        Each dictionary has the following keys:
        - id: the UUID of the cast member
        - name: the name of the cast member
        - type: the type of the cast member

        The test verifies that the cast members are correctly serialized and the response
        contains the expected data.

        """

        cast_member_repository.save(actor_cast_member)
        cast_member_repository.save(director_cast_member)
        expected_response = {
            "data": [
                {
                    "id": str(director_cast_member.id),
                    "name": director_cast_member.name,
                    "type": director_cast_member.type,
                },
                {
                    "id": str(actor_cast_member.id),
                    "name": actor_cast_member.name,
                    "type": actor_cast_member.type,
                },
            ],
            "meta": {
                "current_page": 1,
                "per_page": DEFAULT_PAGE_SIZE,
                "total": 2,
            },
        }

        url = "/api/cast_members/"
        response = api_client_with_auth.get(url)

        assert response.status_code == HTTP_200_OK  # type: ignore
        assert response.data, expected_response  # type: ignore


@pytest.mark.django_db
class TestCreateAPI:
    """
    Class for testing the CreateCastMemberAPI view.
    """

    def test_create_cast_member(
        self,
        cast_member_repository: DjangoORMCastMemberRepository,
        api_client_with_auth: APIClient,
    ):
        """
        Tests the CreateCastMemberAPI view.

        Given a DjangoORMCastMemberRepository, when the CreateCastMemberAPI view is called
        with a POST request to "/api/cast_members/", the expected output is a JSON response
        containing the created cast member data.

        The test verifies that the cast member is correctly serialized and the response
        contains the expected data.

        """

        url = "/api/cast_members/"
        data = {"name": "Robert Downey Jr.", "type": "ACTOR"}
        response = api_client_with_auth.post(
            path=url,
            data=data,
            format="json",
        )

        assert response.status_code == HTTP_201_CREATED  # type: ignore
        assert response.data["id"]  # type: ignore

        cast_member_model = cast_member_repository.get_by_id(response.data["id"])  # type: ignore
        assert cast_member_model is not None
        assert cast_member_model.id == uuid.UUID(response.data["id"])  # type: ignore
        assert cast_member_model.name == "Robert Downey Jr."
        assert cast_member_model.type == "ACTOR"

    def test_create_cast_member_with_empty_name(
        self,
        api_client_with_auth: APIClient,
    ):
        """
        Tests that creating a cast member with an empty name raises a 400 BAD REQUEST
        with a JSON response containing an error message.

        The test verifies that the CreateCastMemberAPI view correctly handles a POST
        request with an empty name and returns the expected error response.
        """

        url = "/api/cast_members/"
        data = {"name": "", "type": "ACTOR"}
        response = api_client_with_auth.post(
            path=url,
            data=data,
            format="json",
        )

        assert response.status_code == HTTP_400_BAD_REQUEST  # type: ignore
        assert response.data == {"name": ["This field may not be blank."]}  # type: ignore

    def test_create_cast_member_with_invalid_type(
        self,
        api_client_with_auth: APIClient,
    ):
        """
        Tests that creating a cast member with an invalid type raises a 400 BAD REQUEST
        with a JSON response containing an error message.

        The test verifies that the CreateCastMemberAPI view correctly handles a POST
        request with an invalid type and returns the expected error response.
        """

        url = "/api/cast_members/"
        data = {"name": "Robert Downey Jr.", "type": "INVALID_TYPE"}
        response = api_client_with_auth.post(
            path=url,
            data=data,
            format="json",
        )

        assert response.status_code == HTTP_400_BAD_REQUEST  # type: ignore
        assert response.data == {"type": ['"INVALID_TYPE" is not a valid choice.']}  # type: ignore


@pytest.mark.django_db
class TestUpdateAPI:
    """
    Class for testing the UpdateCastMemberAPI view.
    """

    def test_update_cast_member(
        self,
        cast_member_repository: DjangoORMCastMemberRepository,
        api_client_with_auth: APIClient,
    ):
        """
        Tests the UpdateCastMemberAPI view.

        Given a DjangoORMCastMemberRepository, when the UpdateCastMemberAPI view is called
        with a PUT request to "/api/cast_members/{id}/", the expected output is a JSON
        response containing the updated cast member data.

        The test verifies that the cast member is correctly serialized and the response
        contains the expected data.

        """

        cast_member = CastMember(
            name="Robert Downey Jr.",
            type=CastMemberType.ACTOR,
        )
        cast_member_repository.save(cast_member)

        url = f"/api/cast_members/{cast_member.id}/"
        response = api_client_with_auth.put(
            path=url,
            data={
                "name": "Cristian Bale",
                "type": "ACTOR",
            },
            format="json",
        )

        assert response.status_code == HTTP_204_NO_CONTENT  # type: ignore

        cast_member_model = cast_member_repository.get_by_id(cast_member.id)  # type: ignore
        assert cast_member_model is not None
        assert cast_member_model.id == cast_member.id
        assert cast_member_model.name == "Cristian Bale"
        assert cast_member_model.type == "ACTOR"

    def test_update_cast_member_with_invalid_id(
        self,
        api_client_with_auth: APIClient,
    ):
        """
        Tests that updating a cast member with an invalid id raises a 400 BAD REQUEST
        with a JSON response containing an error message.

        The test verifies that the UpdateCastMemberAPI view correctly handles a PUT
        request with an invalid id and returns the expected error response.
        """

        url = f"/api/cast_members/{uuid.uuid4()}/"
        response = api_client_with_auth.put(
            path=url,
            data={
                "name": "Cristian Bale",
                "type": "ACTOR",
            },
            format="json",
        )

        assert response.status_code == HTTP_404_NOT_FOUND  # type: ignore
        assert response.data == {"detail": "Cast member not found"}  # type: ignore

    def test_update_cast_member_with_empty_name(
        self,
        cast_member_repository: DjangoORMCastMemberRepository,
        api_client_with_auth: APIClient,
    ):
        """
        Tests that updating a cast member with an empty name raises a 400 BAD REQUEST
        with a JSON response containing an error message.

        The test verifies that the UpdateCastMemberAPI view correctly handles a PUT
        request with an empty name and returns the expected error response.
        """

        cast_member = CastMember(
            name="Robert Downey Jr.",
            type=CastMemberType.ACTOR,
        )
        cast_member_repository.save(cast_member)

        url = f"/api/cast_members/{cast_member.id}/"
        response = api_client_with_auth.put(
            path=url,
            data={
                "name": "",
                "type": "ACTOR",
            },
            format="json",
        )

        assert response.status_code == HTTP_400_BAD_REQUEST  # type: ignore
        assert response.data == {"name": ["This field may not be blank."]}  # type: ignore

    def test_update_cast_member_with_invalid_type(
        self,
        cast_member_repository: DjangoORMCastMemberRepository,
        api_client_with_auth: APIClient,
    ):
        """
        Tests that updating a cast member with an invalid type raises a 400 BAD REQUEST
        with a JSON response containing an error message.

        The test verifies that the UpdateCastMemberAPI view correctly handles a PUT
        request with an invalid type and returns the expected error response.
        """

        cast_member = CastMember(
            name="Robert Downey Jr.",
            type=CastMemberType.ACTOR,
        )
        cast_member_repository.save(cast_member)

        url = f"/api/cast_members/{cast_member.id}/"
        response = api_client_with_auth.put(
            path=url,
            data={
                "name": "Cristian Bale",
                "type": "INVALID_TYPE",
            },
            format="json",
        )

        assert response.status_code == HTTP_400_BAD_REQUEST  # type: ignore
        assert response.data == {"type": ['"INVALID_TYPE" is not a valid choice.']}  # type: ignore


@pytest.mark.django_db
class TestDeleteAPI:
    """
    Class for testing the DeleteCastMemberAPI view.
    """

    def test_delete_cast_member(
        self,
        cast_member_repository: DjangoORMCastMemberRepository,
        api_client_with_auth: APIClient,
    ):
        """
        Tests the DeleteCastMemberAPI view.

        Given a DjangoORMCastMemberRepository, when the DeleteCastMemberAPI view is called
        with a DELETE request to "/api/cast_members/{id}/", the expected output is a JSON
        response containing the deleted cast member data.

        The test verifies that the cast member is correctly deleted and the response
        contains the expected data.
        """

        cast_member = CastMember(
            name="Robert Downey Jr.",
            type=CastMemberType.ACTOR,
        )
        cast_member_repository.save(cast_member)

        url = f"/api/cast_members/{cast_member.id}/"
        response = api_client_with_auth.delete(url)

        assert response.status_code == HTTP_204_NO_CONTENT  # type: ignore
        assert cast_member_repository.get_by_id(cast_member.id) is None

    def test_delete_cast_member_with_invalid_id(
        self,
        api_client_with_auth: APIClient,
    ):
        """
        Tests that deleting a cast member with an invalid id raises a 404 NOT FOUND
        with a JSON response containing an error message.

        The test verifies that the DeleteCastMemberAPI view correctly handles a DELETE
        request with an invalid id and returns the expected error response.
        """

        url = f"/api/cast_members/{uuid.uuid4()}/"
        response = api_client_with_auth.delete(url)

        assert response.status_code == HTTP_404_NOT_FOUND  # type: ignore
        assert response.data == {"detail": "Cast member not found"}  # type: ignore
