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
                    "id": str(actor_cast_member.id),
                    "name": actor_cast_member.name,
                    "type": actor_cast_member.type,
                },
                {
                    "id": str(director_cast_member.id),
                    "name": director_cast_member.name,
                    "type": director_cast_member.type,
                },
            ]
        }

        url = "/api/cast_members/"
        response = APIClient().get(url)

        assert response.status_code == HTTP_200_OK  # type: ignore
        assert response.data == expected_response  # type: ignore


@pytest.mark.django_db
class TestCreateAPI:
    """
    Class for testing the CreateCastMemberAPI view.
    """

    def test_create_cast_member(
        self,
        cast_member_repository: DjangoORMCastMemberRepository,
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
        response = APIClient().post(
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

    def test_create_cast_member_with_empty_name(self):
        """
        Tests that creating a cast member with an empty name raises a 400 BAD REQUEST
        with a JSON response containing an error message.

        The test verifies that the CreateCastMemberAPI view correctly handles a POST
        request with an empty name and returns the expected error response.
        """

        url = "/api/cast_members/"
        data = {"name": "", "type": "ACTOR"}
        response = APIClient().post(
            path=url,
            data=data,
            format="json",
        )

        assert response.status_code == HTTP_400_BAD_REQUEST  # type: ignore
        assert response.data == {"name": ["This field may not be blank."]}  # type: ignore

    def test_create_cast_member_with_invalid_type(self):
        """
        Tests that creating a cast member with an invalid type raises a 400 BAD REQUEST
        with a JSON response containing an error message.

        The test verifies that the CreateCastMemberAPI view correctly handles a POST
        request with an invalid type and returns the expected error response.
        """

        url = "/api/cast_members/"
        data = {"name": "Robert Downey Jr.", "type": "INVALID_TYPE"}
        response = APIClient().post(
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
        response = APIClient().put(
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

    def test_update_cast_member_with_invalid_id(self):
        """
        Tests that updating a cast member with an invalid id raises a 400 BAD REQUEST
        with a JSON response containing an error message.

        The test verifies that the UpdateCastMemberAPI view correctly handles a PUT
        request with an invalid id and returns the expected error response.
        """

        url = f"/api/cast_members/{uuid.uuid4()}/"
        response = APIClient().put(
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
        response = APIClient().put(
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
        response = APIClient().put(
            path=url,
            data={
                "name": "Cristian Bale",
                "type": "INVALID_TYPE",
            },
            format="json",
        )

        assert response.status_code == HTTP_400_BAD_REQUEST  # type: ignore
        assert response.data == {"type": ['"INVALID_TYPE" is not a valid choice.']}  # type: ignore
