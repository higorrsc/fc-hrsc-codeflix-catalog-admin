import uuid

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.test import APIClient

from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.category.domain.category import Category
from src.core.genre.domain.genre import Genre
from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.genre_app.repository import DjangoORMGenreRepository


@pytest.mark.django_db
class TestCreateEditUpdateDeleteAndUploadVideo:
    """
    Test class for testing user can create, edit and delete a video with file upload
    """

    def test_user_can_create_edit_update_delete_and_upload_video(self):
        """
        Verify that a user can create, edit, update, delete, and upload a video,
        and that the edited video data is correct.

        This test creates a video, verifies that it was created, updates the video,
        verifies that it was updated, deletes the video, and verifies that it was
        deleted.
        """

        category_repository = DjangoORMCategoryRepository()
        genre_repository = DjangoORMGenreRepository()
        cast_member_repository = DjangoORMCastMemberRepository()

        movie_category_id = uuid.uuid4()
        genre_action_id = uuid.uuid4()
        genre_adventure_id = uuid.uuid4()
        cast_member_actor_id = uuid.uuid4()
        cast_member_director_id = uuid.uuid4()

        category_repository.save(
            Category(
                id=movie_category_id,
                name="Movie",
                description="Movies category",
            )
        )

        genre_repository.save(
            Genre(
                id=genre_action_id,
                name="Action",
                categories={movie_category_id},
            )
        )
        genre_repository.save(
            Genre(
                id=genre_adventure_id,
                name="Adventure",
                categories={movie_category_id},
            )
        )

        cast_member_repository.save(
            CastMember(
                id=cast_member_actor_id,
                name="Sam Worthington",
                type=CastMemberType.ACTOR,
            )
        )
        cast_member_repository.save(
            CastMember(
                id=cast_member_director_id,
                name="James Cameron",
                type=CastMemberType.DIRECTOR,
            )
        )

        api_client = APIClient()
        list_response = api_client.get("/api/videos/")
        assert list_response.status_code == HTTP_200_OK  # type: ignore

        data = {
            "title": "Avatar",
            "description": "A marine on an alien planet",
            "duration": 162,
            "launch_year": 2009,
            "rating": "AGE_14",
            "categories": [
                str(movie_category_id),
            ],
            "genres": [
                str(genre_action_id),
                str(genre_adventure_id),
            ],
            "cast_members": [
                str(cast_member_actor_id),
                str(cast_member_director_id),
            ],
        }

        create_response = api_client.post(
            path="/api/videos/",
            data=data,
            format="json",
        )
        assert create_response.status_code == HTTP_201_CREATED  # type: ignore
        assert create_response.data["id"]  # type: ignore

        video_id = create_response.data["id"]  # type: ignore

        list_response = api_client.get("/api/videos/")
        assert list_response.status_code == HTTP_200_OK  # type: ignore
        assert len(list_response.data["data"]) == 1  # type: ignore

        updated_data = {
            "title": "Avatar Updated",
            "description": "A marine on an alien planet",
            "duration": 162,
            "launch_year": 2009,
            "published": True,
            "rating": "AGE_14",
            "categories": [
                str(movie_category_id),
            ],
            "genres": [
                str(genre_adventure_id),
            ],
            "cast_members": [
                str(cast_member_director_id),
            ],
        }

        update_response = api_client.put(
            path=f"/api/videos/{video_id}/",
            data=updated_data,
            format="json",
        )

        assert update_response.status_code == HTTP_204_NO_CONTENT  # type: ignore

        list_response = api_client.get("/api/videos/")
        assert list_response.status_code == HTTP_200_OK  # type: ignore
        assert len(list_response.data["data"]) == 1  # type: ignore
        assert list_response.data["data"], updated_data  # type: ignore

        upload_file = SimpleUploadedFile(
            "video.mp4",
            b"Fake video content",
            "video/mp4",
        )
        upload_data = {
            "video_file": upload_file,
        }
        patch_response = api_client.patch(
            path=f"/api/videos/{video_id}/",
            data=upload_data,
            format="multipart",
        )
        assert patch_response.status_code == HTTP_200_OK  # type: ignore

        delete_response = api_client.delete(path=f"/api/videos/{video_id}/")
        assert delete_response.status_code == HTTP_204_NO_CONTENT  # type: ignore

        list_response = api_client.get("/api/videos/")
        assert list_response.status_code == HTTP_200_OK  # type: ignore
        assert len(list_response.data["data"]) == 0  # type: ignore
