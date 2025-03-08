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


@pytest.mark.django_db
class TestGetById:
    """
    Test class for the DjangoORMGenreRepository.get_by_id method.
    """

    def test_retrieves_genre_from_database(self):
        """
        Retrieves a Genre from the database by its ID.

        This test verifies that the `get_by_id` method of the DjangoORMGenreRepository
        successfully retrieves a Genre from the database, ensuring that the correct
        Genre is returned when queried by its ID.

        Asserts:
            retrieved_genre is not None
        """

        genre = Genre(name="Action")
        genre_repository = DjangoORMGenreRepository()
        genre_repository.save(genre)

        retrieved_genre = genre_repository.get_by_id(genre.id)
        assert retrieved_genre is not None
        assert retrieved_genre.id == genre.id
        assert retrieved_genre.name == "Action"
        assert retrieved_genre.is_active is True

    def test_retrieves_genre_with_categories_from_database(self):
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

        retrieved_genre = genre_repository.get_by_id(genre.id)
        assert retrieved_genre is not None
        assert retrieved_genre.id == genre.id
        assert retrieved_genre.name == "Action"
        assert retrieved_genre.is_active is True
        assert retrieved_genre.categories == {movie_category.id}


@pytest.mark.django_db
class TestDelete:
    """
    Test class for the DjangoORMGenreRepository.delete method.
    """

    def test_deletes_genre_from_database(self):
        """
        Deletes a Genre from the database by its ID.

        This test verifies that the `delete` method of the DjangoORMGenreRepository
        successfully deletes a Genre from the database, ensuring that the Genre is
        removed when queried by its ID.

        Asserts:
            GenreORM.objects.count() == 0
        """
        genre = Genre(name="Action")
        genre_repository = DjangoORMGenreRepository()
        genre_repository.save(genre)
        assert GenreORM.objects.count() == 1

        genre_repository.delete(genre.id)
        assert GenreORM.objects.count() == 0

    def test_deletes_genre_with_categories_from_database(self):
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

        genre_repository.delete(genre.id)
        assert GenreORM.objects.count() == 0

        retrieved_genre = genre_repository.get_by_id(genre.id)
        assert retrieved_genre is None


@pytest.mark.django_db
class TestUpdate:
    """
    Test class for the DjangoORMGenreRepository.update method.
    """

    def test_updates_genre_in_database(self):
        genre = Genre(name="Action")
        genre_repository = DjangoORMGenreRepository()
        genre_repository.save(genre)

        genre.name = "Adventure"
        genre.deactivate()
        genre_repository.update(genre)

        genre_from_db = GenreORM.objects.get(id=genre.id)
        assert genre_from_db.id == genre.id
        assert genre_from_db.name == "Adventure"
        assert genre_from_db.is_active is False

    def test_updates_genre_with_categories_in_database(self):
        """
        Updates a Genre with associated categories in the database.

        This test verifies that the `update` method of the DjangoORMGenreRepository
        successfully updates a Genre with the provided name and category IDs,
        ensuring that the Genre is updated in the database with the correct data
        and associated categories.

        Asserts:
            GenreORM.objects.count() == 1
            GenreORM.objects.get(id=genre.id).id == genre.id
            GenreORM.objects.get(id=genre.id).name == "Adventure"
            GenreORM.objects.get(id=genre.id).is_active is False
            GenreORM.objects.get(id=genre.id).categories.count() == 2
            GenreORM.objects.get(id=genre.id).categories.count() == 1
        """

        movie_category = Category(
            name="Movie",
            description="Movies category",
        )
        anime_category = Category(
            name="Anime",
            description="Anime category",
        )
        category_repository = DjangoORMCategoryRepository()
        category_repository.save(movie_category)
        category_repository.save(anime_category)

        genre = Genre(
            name="Action",
            categories={movie_category.id},
        )
        genre_repository = DjangoORMGenreRepository()
        genre_repository.save(genre)

        genre.name = "Adventure"
        genre.deactivate()
        genre.add_category(anime_category.id)
        genre_repository.update(genre)

        genre_from_db = GenreORM.objects.get(id=genre.id)
        assert genre_from_db.id == genre.id
        assert genre_from_db.name == "Adventure"
        assert genre_from_db.is_active is False
        assert genre_from_db.categories.count() == 2

        genre.remove_category(anime_category.id)
        genre_repository.update(genre)

        genre_from_db = GenreORM.objects.get(id=genre.id)
        assert genre_from_db.categories.count() == 1


@pytest.mark.django_db
class TestList:
    """
    Test class for the DjangoORMGenreRepository.list method.
    """

    def test_lists_genres_from_database(self):
        """
        Tests listing genres from the database.

        This test verifies that the `list` method of the DjangoORMGenreRepository
        returns a list of genres from the database, ensuring that the genres are
        retrieved with the correct data.

        Asserts:
            len(genres) == 1
            genres[0].id == genre.id
            genres[0].name == "Action"
            genres[0].is_active is True
        """

        genre = Genre(name="Action")
        genre_repository = DjangoORMGenreRepository()
        genre_repository.save(genre)

        genres = genre_repository.list()
        assert len(genres) == 1
        assert genres[0].id == genre.id
        assert genres[0].name == "Action"
        assert genres[0].is_active is True

    def test_lists_genres_with_categories_from_database(self):
        """
        Lists Genres with associated categories from the database.

        This test verifies that the `list` method of the DjangoORMGenreRepository
        successfully lists Genres with associated categories, ensuring that the
        Genres are retrieved from the database with the correct data and
        associated categories.

        Asserts:
            len(genres) == 1
            genres[0].id == genre.id
            genres[0].name == "Action"
            genres[0].is_active is True
            movie_category.id in genres[0].categories
        """
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

        genres = genre_repository.list()
        assert len(genres) == 1
        assert genres[0].id == genre.id
        assert genres[0].name == "Action"
        assert genres[0].is_active is True
        assert movie_category.id in genres[0].categories
