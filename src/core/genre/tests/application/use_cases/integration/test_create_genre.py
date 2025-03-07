import uuid

import pytest

from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
)
from src.core.genre.application.exceptions import RelatedCategoriesNotFound
from src.core.genre.application.use_cases.create_genre import CreateGenre
from src.core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository


@pytest.fixture
def movie_category() -> Category:
    """
    Fixture for a Category instance representing movies.

    Returns:
        Category: A Category object with name "Movie" and description "Movies category".
    """

    return Category(
        name="Movie",
        description="Movies category",
    )


@pytest.fixture
def documentary_category() -> Category:
    """
    Fixture for a Category instance representing documentaries.

    Returns:
        Category: A Category object with name "Documentary" and description "Documentary category".
    """

    return Category(
        name="Documentary",
        description="Documentary category",
    )


@pytest.fixture
def category_repository(movie_category, documentary_category) -> CategoryRepository:
    return InMemoryCategoryRepository(
        [
            movie_category,
            documentary_category,
        ]
    )


class TesteCreateGenre:
    """
    Test the CreateGenre class.
    """

    def test_create_genre_with_associated_categories(
        self,
        movie_category,
        documentary_category,
        category_repository,
    ):
        """
        Test the creation of a Genre with associated categories.

        This test verifies that the `create_genre` use case successfully creates a
        genre with the provided name and category IDs, ensuring that the genre is
        saved in the repository with the correct data.

        Args:
            movie_category (Category): A Category object with name "Movie".
            documentary_category (Category): A Category object with name "Documentary".
            category_repository (CategoryRepository): An in-memory CategoryRepository
            containing the movie and documentary categories.
        """

        genre_repository = InMemoryGenreRepository()

        use_case = CreateGenre(
            genre_repository=genre_repository,
            category_repository=category_repository,
        )
        input = CreateGenre.Input(
            name="Action",
            category_ids={movie_category.id, documentary_category.id},
        )

        output = use_case.execute(input)

        assert output.id is not None
        assert isinstance(output.id, uuid.UUID)

        saved_genre = genre_repository.get_by_id(output.id)
        assert saved_genre.name == input.name  # type: ignore
        assert saved_genre.is_active is True  # type: ignore
        assert saved_genre.categories == input.category_ids  # type: ignore

    def test_create_genre_with_inexistent_categories_raise_an_error(
        self,
        category_repository,
    ):
        """
        Test the creation of a Genre with inexistent categories.

        This test verifies that the `create_genre` use case raises an error when
        the input includes categories that are not found in the category repository.

        Args:
            category_repository (CategoryRepository): An in-memory CategoryRepository
            containing the movie and documentary categories.
        """

        genre_repository = InMemoryGenreRepository()

        use_case = CreateGenre(
            genre_repository=genre_repository,
            category_repository=category_repository,
        )
        input = CreateGenre.Input(
            name="Action",
            category_ids={
                uuid.uuid4(),
                uuid.uuid4(),
            },
        )

        with pytest.raises(RelatedCategoriesNotFound) as exc_info:
            use_case.execute(input)

        assert len(genre_repository.list()) == 0
        assert str(input.category_ids) in str(exc_info.value)

    def test_create_genre_without_categories(self):
        """
        Test the creation of a Genre without categories.

        This test verifies that the `create_genre` use case successfully creates a
        genre without categories, ensuring that the genre is saved in the repository
        with the correct data.
        """

        genre_repository = InMemoryGenreRepository()
        category_repository = InMemoryCategoryRepository()

        use_case = CreateGenre(
            genre_repository=genre_repository,
            category_repository=category_repository,
        )
        input = CreateGenre.Input(
            name="Action",
        )

        output = use_case.execute(input)

        assert output.id is not None
        assert isinstance(output.id, uuid.UUID)

        saved_genre = genre_repository.get_by_id(output.id)
        assert saved_genre.name == input.name  # type: ignore
        assert saved_genre.is_active is True  # type: ignore
        assert saved_genre.categories == set()  # type: ignore
