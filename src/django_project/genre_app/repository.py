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

        try:
            genre_model = GenreORM.objects.get(pk=genre_id)
        except GenreORM.DoesNotExist:
            return None

        return Genre(
            id=genre_model.id,
            name=genre_model.name,
            is_active=genre_model.is_active,
            categories={category.id for category in genre_model.categories.all()},
        )

    def delete(self, genre_id: uuid.UUID):
        """
        Delete a genre by its ID from the repository.

        Args:
            id (uuid.UUID): The ID of the genre to be deleted.
        """

        try:
            GenreORM.objects.filter(pk=genre_id).delete()
        except GenreORM.DoesNotExist:
            return None

    def update(self, genre: Genre):
        """
        Update a genre in the repository.

        Args:
            genre (Genre): The genre to be updated.
        """

        try:
            genre_model = GenreORM.objects.get(pk=genre.id)
        except GenreORM.DoesNotExist:
            return None

        with transaction.atomic():
            genre_model.name = genre.name
            genre_model.is_active = genre.is_active
            genre_model.save()
            genre_model.categories.set(genre.categories)

    def list(self) -> List[Genre]:
        """
        List all categories from the repository.

        Returns:
            list[Genre]: A list of all categories.
        """

        return [
            Genre(
                id=genre.id,
                name=genre.name,
                is_active=genre.is_active,
                categories={category.id for category in genre.categories.all()},
            )
            for genre in GenreORM.objects.all()
        ]
