import threading
import time
from pathlib import Path

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.test import APIClient

from src.core.video.domain.value_objects import MediaStatus, MediaType
from src.core.video.infra.video_converted_consumer import VideoConvertedRabbitMQConsumer
from src.core.video.infra.video_converted_producer import VideoConvertedRabbitMQProducer


@pytest.mark.django_db(transaction=True)
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

        consumer = VideoConvertedRabbitMQConsumer()
        thread = threading.Thread(target=consumer.start, daemon=True)
        thread.start()

        api_client = APIClient()

        category_response = api_client.post(
            path="/api/categories/",
            data={
                "name": "Movie",
                "description": "Movies category",
            },
            format="json",
        )
        assert category_response.status_code == HTTP_201_CREATED  # type: ignore
        assert category_response.data["id"] is not None  # type: ignore
        movie_category_id = category_response.data["id"]  # type: ignore

        genre_response = api_client.post(
            path="/api/genres/",
            data={
                "name": "Action",
                "categories": [movie_category_id],
            },
            format="json",
        )
        assert genre_response.status_code == HTTP_201_CREATED  # type: ignore
        assert genre_response.data["id"] is not None  # type: ignore
        action_genre_id = genre_response.data["id"]  # type: ignore

        genre_response = api_client.post(
            path="/api/genres/",
            data={
                "name": "Adventure",
                "categories": [movie_category_id],
            },
            format="json",
        )
        assert genre_response.status_code == HTTP_201_CREATED  # type: ignore
        assert genre_response.data["id"] is not None  # type: ignore
        adventure_genre_id = genre_response.data["id"]  # type: ignore

        actor_cast_member_response = api_client.post(
            path="/api/cast_members/",
            data={
                "name": "Sam Worthington",
                "type": "ACTOR",
            },
            format="json",
        )
        assert actor_cast_member_response.status_code == HTTP_201_CREATED  # type: ignore
        assert actor_cast_member_response.data["id"] is not None  # type: ignore
        actor_cast_member_id = actor_cast_member_response.data["id"]  # type: ignore

        director_cast_member_response = api_client.post(
            path="/api/cast_members/",
            data={
                "name": "James Cameron",
                "type": "DIRECTOR",
            },
            format="json",
        )
        assert director_cast_member_response.status_code == HTTP_201_CREATED  # type: ignore
        assert director_cast_member_response.data["id"] is not None  # type: ignore
        director_cast_member_id = director_cast_member_response.data["id"]  # type: ignore

        list_response = api_client.get("/api/videos/")
        assert list_response.status_code == HTTP_200_OK  # type: ignore

        create_response = api_client.post(
            path="/api/videos/",
            data={
                "title": "Avatar",
                "description": "A marine on an alien planet",
                "duration": 162,
                "launch_year": 2009,
                "rating": "AGE_14",
                "categories": [movie_category_id],
                "genres": [action_genre_id, adventure_genre_id],
                "cast_members": [actor_cast_member_id, director_cast_member_id],
            },
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
            "published": False,
            "rating": "AGE_14",
            "categories": [movie_category_id],
            "genres": [adventure_genre_id],
            "cast_members": [director_cast_member_id],
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

        patch_response = api_client.patch(
            path=f"/api/videos/{video_id}/",
            data={
                "video_file": SimpleUploadedFile(
                    name="video.mp4",
                    content=b"Fake video content",
                    content_type="video/mp4",
                ),
            },
            format="multipart",
        )
        assert patch_response.status_code == HTTP_200_OK  # type: ignore

        raw_path = Path("videos") / str(video_id) / "video.mp4"
        get_response = api_client.get(f"/api/videos/{video_id}/")
        assert get_response.status_code == HTTP_200_OK  # type: ignore
        assert get_response.data["id"] == video_id  # type: ignore
        assert get_response.data["video"] == {  # type: ignore
            "name": "video.mp4",
            "raw_location": str(raw_path),
            "encoded_location": "",
            "status": "PENDING",
            "media_type": "VIDEO",
            "check_sum": "",
        }

        producer = VideoConvertedRabbitMQProducer()
        message = {
            "error": "",
            "video": {
                "resource_id": f"{video_id}.{MediaType.VIDEO}",
                "encoded_video_folder": "/path/to/encoded/video",
            },
            "status": MediaStatus.COMPLETED,
        }
        producer.publish(message=message)
        producer.close()

        time.sleep(10)
        thread.join(timeout=10)

        get_response = api_client.get(f"/api/videos/{video_id}/")
        assert get_response.status_code == HTTP_200_OK  # type: ignore
        assert get_response.data["id"] == video_id  # type: ignore
        assert get_response.data["video"] == {  # type: ignore
            "name": "video.mp4",
            "raw_location": str(raw_path),
            "encoded_location": "/path/to/encoded/video",
            "status": "COMPLETED",
            "media_type": "VIDEO",
            "check_sum": "",
        }
        delete_response = api_client.delete(path=f"/api/videos/{video_id}/")
        assert delete_response.status_code == HTTP_204_NO_CONTENT  # type: ignore

        list_response = api_client.get("/api/videos/")
        assert list_response.status_code == HTTP_200_OK  # type: ignore
        assert len(list_response.data["data"]) == 0  # type: ignore
