from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
)
from src.core.genre.application.use_cases.list_genre import GenreOutput, ListGenre
from src.core.genre.domain.genre import Genre
from src.core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository


class TestListGenre:
    """
    Test the `ListGenre` use case.
    """

    def test_list_genres_with_associated_categories(self):
        """
        When calling list_genres() with associated categories, it returns a
        list of GenreOutput objects containing the name and associated categories
        of each genre in the repository.

        Args:
            None

        Returns:
            ListGenre.Output: A list of GenreOutput objects.
        """

        movie_category = Category(name="Movie")
        documentary_category = Category(name="Documentary")
        category_repository = InMemoryCategoryRepository()
        category_repository.save(movie_category)
        category_repository.save(documentary_category)

        genre_repository = InMemoryGenreRepository()
        genre = Genre(
            name="Drama",
            categories={
                movie_category.id,  # type: ignore
                documentary_category.id,  # type: ignore
            },
        )
        genre_repository.save(genre)

        use_case = ListGenre(repository=genre_repository)
        output = use_case.execute(input=ListGenre.Input())

        assert len(output.data) == 1
        assert output == ListGenre.Output(
            data=[
                GenreOutput(
                    id=genre.id,
                    name=genre.name,
                    is_active=genre.is_active,
                    categories={
                        movie_category.id,
                        documentary_category.id,
                    },
                )
            ]
        )

    def test_list_genres_without_associated_categories(self):
        """
        When calling list_genres() without associated categories, it returns a
        list of GenreOutput objects containing the name and associated categories
        of each genre in the repository.

        Args:
            None

        Returns:
            ListGenre.Output: A list of GenreOutput objects.
        """

        genre_repository = InMemoryGenreRepository()
        genre = Genre(name="Drama")
        genre_repository.save(genre)

        use_case = ListGenre(repository=genre_repository)
        output = use_case.execute(input=ListGenre.Input())

        assert len(output.data) == 1
        assert output == ListGenre.Output(
            data=[
                GenreOutput(
                    id=genre.id,
                    name=genre.name,
                    is_active=genre.is_active,
                    categories=set(),
                )
            ]
        )

    def test_list_genres_empty_repository(self):
        """
        When calling list_genres() with an empty repository, it returns an empty
        list of GenreOutput objects.

        Args:
            None

        Returns:
            ListGenre.Output: An empty list of GenreOutput objects.
        """

        genre_repository = InMemoryGenreRepository()

        use_case = ListGenre(repository=genre_repository)
        output = use_case.execute(input=ListGenre.Input())

        assert len(output.data) == 0
        assert output == ListGenre.Output(data=[])
