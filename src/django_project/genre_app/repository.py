import uuid
from typing import List

from django.db import transaction

from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository
from src.django_project.genre_app.models import Genre as GenreORM


class DjangoORMGenreRepository(GenreRepository):
    """
    Django ORM implementation of the GenreRepository interface.
    """

    def __init__(self, genre_model: GenreORM | None = None):
        self.genre_model = genre_model or GenreORM

    def save(self, genre: Genre):
        """
        Save a genre to the repository.

        Args:
            genre (Genre): The genre to be saved.
        """

        with transaction.atomic():
            genre_model = GenreORM.objects.create(
                id=genre.id,
                name=genre.name,
                is_active=genre.is_active,
            )
            genre_model.categories.set(genre.categories)

    def get_by_id(self, genre_id: uuid.UUID) -> Genre | None:
        """
        Retrieve a genre by its ID from the repository.

        Args:
            id (uuid.UUID): The ID of the genre to be retrieved.

        Returns:
            Genre: The genre with the given ID, or None if it doesn't exist.
        """
        raise NotImplementedError

    def delete(self, genre_id: uuid.UUID):
        """
        Delete a genre by its ID from the repository.

        Args:
            id (uuid.UUID): The ID of the genre to be deleted.
        """
        raise NotImplementedError

    def update(self, genre: Genre):
        """
        Update a genre in the repository.

        Args:
            genre (Genre): The genre to be updated.
        """
        raise NotImplementedError

    def list(self) -> List[Genre]:
        """
        List all categories from the repository.

        Returns:
            list[Genre]: A list of all categories.
        """
        raise NotImplementedError
