from src.config import DEFAULT_PAGE_SIZE
from src.core._shared.application.use_cases.list import (
    ListRequest,
    ListResponse,
    ListResponseMeta,
)
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
)
from src.core.genre.application.use_cases.list_genre import ListGenre
from src.core.genre.domain.genre import Genre
from src.core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository


class TestListGenre:
    """
    Test the `ListGenre` use case.
    """

    def test_list_genres_with_associated_categories(self):
        """
        When calling list_genres() with associated categories, it returns a
        ListResponse containing the genres with their associated categories.

        This test verifies that the `list_genres` use case successfully lists the
        genres with their associated categories, ensuring that the genres and
        categories are retrieved from the repository with the correct data.
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
        output: ListResponse = use_case.execute(ListRequest(order_by="name"))

        assert len(output["data"]) == 1  # type: ignore
        assert output == {
            "data": [genre],
            "meta": ListResponseMeta(
                current_page=1,
                per_page=DEFAULT_PAGE_SIZE,
                total=1,
            ),
        }

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
        output: ListResponse = use_case.execute(ListRequest(order_by="name"))

        assert len(output["data"]) == 1  # type: ignore
        assert output == {
            "data": [genre],
            "meta": ListResponseMeta(
                current_page=1,
                per_page=DEFAULT_PAGE_SIZE,
                total=1,
            ),
        }

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
        output: ListResponse = use_case.execute(ListRequest(order_by="name"))

        assert len(output["data"]) == 0  # type: ignore
        assert output == {
            "data": [],
            "meta": ListResponseMeta(
                current_page=1,
                per_page=DEFAULT_PAGE_SIZE,
                total=0,
            ),
        }
