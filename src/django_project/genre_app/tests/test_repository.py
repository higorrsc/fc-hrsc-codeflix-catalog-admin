import pytest

from src.core.category.domain.category import Category
from src.core.genre.domain.genre import Genre
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.genre_app.models import Genre as GenreORM
from src.django_project.genre_app.repository import DjangoORMGenreRepository


@pytest.mark.django_db
class TestSave:
    """
    Test class for the DjangoORMGenreRepository.save method.
    """

    def test_saves_genre_in_database(self):
        """
        Saves a Genre in the database.

        This test verifies that the `save` method of the DjangoORMGenreRepository
        successfully saves a Genre in the database, ensuring that the Genre is
        persisted with the correct data.

        Args:
            genre (Genre): The Genre to be saved.

        Asserts:
            GenreORM.objects.count() == 1
            GenreORM.objects.get(id=genre.id).id == genre.id
            GenreORM.objects.get(id=genre.id).name == "Action"
            GenreORM.objects.get(id=genre.id).is_active is True
        """

        genre = Genre(name="Action")
        genre_repository = DjangoORMGenreRepository()
        genre_repository.save(genre)
        assert GenreORM.objects.count() == 1

        genre_from_db = GenreORM.objects.get(id=genre.id)
        assert genre_from_db.id == genre.id
        assert genre_from_db.name == "Action"
        assert genre_from_db.is_active is True

    def test_saves_genre_with_categories_in_database(self):
        movie_category = Category(
            name="Movie",
            description="Movies category",
        )
        category_repository = DjangoORMCategoryRepository()
        category_repository.save(movie_category)

        genre = Genre(
            name="Action",
            categories={movie_category.id},
        )
        genre_repository = DjangoORMGenreRepository()
        genre_repository.save(genre)
        assert GenreORM.objects.count() == 1

        genre_from_db = GenreORM.objects.get(id=genre.id)
        assert genre_from_db.id == genre.id
        assert genre_from_db.name == "Action"
        assert genre_from_db.is_active is True
        assert genre_from_db.categories.count() == 1

        related_categories = genre_from_db.categories.all()
        assert related_categories[0].id == movie_category.id
        assert related_categories[0].name == movie_category.name
