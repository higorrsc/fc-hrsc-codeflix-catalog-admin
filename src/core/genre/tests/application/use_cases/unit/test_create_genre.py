import uuid
from unittest.mock import create_autospec

import pytest

from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.application.exceptions import (
    InvalidGenre,
    RelatedCategoriesNotFound,
)
from src.core.genre.application.use_cases.create_genre import CreateGenre
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository


@pytest.fixture
def mock_genre_repository() -> GenreRepository:
    """
    Fixture for a mock GenreRepository instance.

    Returns:
        GenreRepository: A mock GenreRepository object.
    """

    return create_autospec(GenreRepository)


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
def mock_category_repository_with_categories(
    movie_category: Category, documentary_category: Category
) -> CategoryRepository:
    """
    Fixture for a mock CategoryRepository instance that contains the movie and
    documentary categories.

    This fixture is used to provide a mock CategoryRepository that contains the
    movie and documentary categories, which can then be used in tests to verify
    that the get_categories_list use case returns the correct categories.

    Returns:
        CategoryRepository: A mock CategoryRepository that contains the movie
        and documentary categories.
    """

    repository = create_autospec(CategoryRepository)
    repository.list.return_value = [movie_category, documentary_category]
    return repository


@pytest.fixture
def mock_empty_category_repository() -> CategoryRepository:
    """
    Fixture for a mock CategoryRepository instance that contains no categories.

    This fixture is used to provide a mock CategoryRepository that contains no categories,
    which can then be used in tests to verify that the get_categories_list use case returns
    an empty list.

    Returns:
        CategoryRepository: A mock CategoryRepository that contains no categories.
    """

    repository = create_autospec(CategoryRepository)
    repository.list.return_value = []
    return repository


class TesteCreateGenre:
    """
    Test the CreateGenre class.
    """

    def test_when_categories_do_not_exist_then_raise_related_categories_not_found(
        self,
        mock_empty_category_repository: CategoryRepository,
        mock_genre_repository: GenreRepository,
    ):
        """
        When calling create_genre() with a set of category IDs that do not
        exist in the repository, it raises a RelatedCategoriesNotFound exception.

        This test verifies that the `create_genre` use case raises a
        `RelatedCategoriesNotFound` exception when the given category IDs do not exist
        in the repository.
        """
        use_case = CreateGenre(
            genre_repository=mock_genre_repository,
            category_repository=mock_empty_category_repository,
        )
        category_id = uuid.uuid4()
        input = CreateGenre.Input(
            name="Action",
            category_ids={category_id},
        )

        with pytest.raises(RelatedCategoriesNotFound) as exc_info:
            use_case.execute(input)

        assert str(category_id) in str(exc_info.value)

    def test_when_create_genre_is_invalid_then_raise_invalid_genre(
        self,
        movie_category,
        mock_category_repository_with_categories,
        mock_genre_repository,
    ):
        """
        When calling create_genre() with an invalid Genre (e.g. with an empty name),
        it raises an InvalidGenre exception.

        This test verifies that the `create_genre` use case raises an
        `InvalidGenre` exception when the given Genre is invalid.

        Args:
            movie_category (Category): A Category object with name "Movie" and description "Movies category".
            mock_category_repository_with_categories (CategoryRepository): A mock CategoryRepository that contains the movie and documentary categories.
            mock_genre_repository (GenreRepository): A mock GenreRepository object.
        """
        use_case = CreateGenre(
            genre_repository=mock_genre_repository,
            category_repository=mock_category_repository_with_categories,
        )
        input = CreateGenre.Input(
            name="",
            category_ids={movie_category.id},
        )

        with pytest.raises(InvalidGenre) as exc_info:
            use_case.execute(input)

        assert "Name cannot be empty" in str(exc_info.value)

    def test_when_created_genre_is_valid_and_categories_exist_then_save_genre(
        self,
        movie_category,
        documentary_category,
        mock_genre_repository,
        mock_category_repository_with_categories,
    ):
        """
        When creating a Genre with valid data and existing categories,
        it saves the genre in the repository and returns a valid genre ID.

        This test verifies that the `create_genre` use case successfully
        creates a genre with the provided name and category IDs, ensuring
        that the genre is saved in the repository with the correct data.

        Args:
            movie_category (Category): A Category object with name "Movie".
            documentary_category (Category): A Category object with name "Documentary".
            mock_genre_repository (GenreRepository): A mock GenreRepository object.
            mock_category_repository_with_categories (CategoryRepository): A mock
            CategoryRepository containing the movie and documentary categories.
        """

        use_case = CreateGenre(
            genre_repository=mock_genre_repository,
            category_repository=mock_category_repository_with_categories,
        )
        input = CreateGenre.Input(
            name="Romance",
            category_ids={movie_category.id, documentary_category.id},
        )
        output = use_case.execute(input)

        assert isinstance(output.id, uuid.UUID)
        mock_genre_repository.save.assert_called_once_with(
            Genre(
                id=output.id,
                name=input.name,
                is_active=input.is_active,
                categories=input.category_ids,
            )
        )

    def test_when_create_genre_without_categories(
        self,
        mock_genre_repository,
        mock_empty_category_repository,
    ):
        """
        When creating a Genre without providing category IDs, it saves the genre
        in the repository with default empty categories and returns a valid genre ID.

        This test verifies that the `create_genre` use case successfully creates
        a genre with the provided name and default empty categories, ensuring
        that the genre is saved in the repository with the correct data.

        Args:
            mock_genre_repository (GenreRepository): A mock GenreRepository object.
            mock_empty_category_repository (CategoryRepository): A mock CategoryRepository
            that contains no categories.
        """

        use_case = CreateGenre(
            genre_repository=mock_genre_repository,
            category_repository=mock_empty_category_repository,
        )
        input = CreateGenre.Input(
            name="Romance",
        )
        output = use_case.execute(input)

        assert isinstance(output.id, uuid.UUID)
        mock_genre_repository.save.assert_called_once_with(
            Genre(
                id=output.id,
                name=input.name,
                is_active=input.is_active,
            )
        )
