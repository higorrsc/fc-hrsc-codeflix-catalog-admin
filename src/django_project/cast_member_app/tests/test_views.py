import pytest
from rest_framework.status import HTTP_200_OK
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
