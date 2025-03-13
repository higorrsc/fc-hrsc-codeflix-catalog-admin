import uuid
from unittest.mock import create_autospec

import pytest

from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.application.exceptions import (
    GenreNotFound,
    InvalidGenre,
    RelatedCategoriesNotFound,
)
from src.core.genre.application.use_cases.update_genre import UpdateGenre
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository


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
def genre_id() -> uuid.UUID:
    """
    Fixture for a UUID representing a genre ID.

    Returns:
        uuid.UUID: A UUID object.
    """

    return uuid.UUID("6030fb56-cd39-483d-bf09-c0d930c45739")


@pytest.fixture
def horror_genre(
    genre_id: uuid.UUID,
    movie_category: Category,
) -> Genre:
    """
    Fixture for a Genre instance representing Horror movies.

    Returns:
        Genre: A Genre object with name "Horror" and the movie category.
    """

    return Genre(
        id=genre_id,
        name="Horror",
        categories={
            movie_category.id,
        },
    )


@pytest.fixture
def horror_genre_updated(
    genre_id: uuid.UUID,
    movie_category: Category,
    documentary_category: Category,
) -> Genre:
    """
    Fixture for a Genre instance representing Horror movies with the movie and
    documentary categories.

    Returns:
        Genre: A Genre object with name "Horror" and the movie and documentary
        categories.
    """
    return Genre(
        id=genre_id,
        name="Horror Updated",
        is_active=False,
        categories={
            movie_category.id,
            documentary_category.id,
        },
    )


@pytest.fixture
def mock_genre_repository(horror_genre_updated: Genre) -> GenreRepository:
    """
    Fixture for a mock GenreRepository instance.

    Returns:
        GenreRepository: A mock GenreRepository object.
    """

    repository = create_autospec(GenreRepository)
    repository.update.return_value = horror_genre_updated
    return repository


@pytest.fixture
def mock_category_repository_with_categories(
    movie_category: Category,
    documentary_category: Category,
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


class TestUpdateGenre:
    """
    Test suite for the UpdateGenre use case.
    """

    def test_update_not_existing_genre_raises_exception(
        self,
        mock_genre_repository: GenreRepository,
        mock_category_repository_with_categories: CategoryRepository,
    ):
        """
        When calling update_genre() with a non-existent genre ID, it raises a
        GenreNotFound exception.

        This test verifies that the `update_genre` use case raises a
        GenreNotFound exception when the genre is not found in the repository.
        """

        mock_genre_repository.get_by_id.return_value = None  # type: ignore
        use_case = UpdateGenre(
            genre_repository=mock_genre_repository,
            category_repository=mock_category_repository_with_categories,
        )
        with pytest.raises(GenreNotFound, match="Genre with .* not found"):
            use_case.execute(
                input=UpdateGenre.Input(
                    id=uuid.uuid4(),
                    name="Horror",
                    is_active=True,
                    categories=set(),
                )
            )

        mock_genre_repository.update.assert_not_called()  # type: ignore

    def test_update_genre_with_invalid_input_raises_exception(
        self,
        mock_genre_repository: GenreRepository,
        mock_category_repository_with_categories: CategoryRepository,
        horror_genre: Genre,
    ):
        """
        When calling update_genre() with an invalid Genre (e.g. with an empty name),
        it raises an InvalidGenre exception.

        This test verifies that the `update_genre` use case raises an
        `InvalidGenre` exception when the given Genre is invalid.

        Args:
            mock_genre_repository (GenreRepository): A mock GenreRepository object.
            mock_category_repository_with_categories (CategoryRepository): A mock
            CategoryRepository containing the movie and documentary categories.
            horror_genre (Genre): A Genre object with name "Horror".
        """
        mock_genre_repository.get_by_id.return_value = horror_genre  # type: ignore
        use_case = UpdateGenre(
            genre_repository=mock_genre_repository,
            category_repository=mock_category_repository_with_categories,
        )
        with pytest.raises(InvalidGenre, match="Name cannot be empty"):
            use_case.execute(
                input=UpdateGenre.Input(
                    id=uuid.uuid4(),
                    name="",
                    is_active=True,
                    categories=set(),
                )
            )

        mock_genre_repository.update.assert_not_called()  # type: ignore

    def test_update_genre_with_invalid_related_categories_raises_exception(
        self,
        mock_genre_repository: GenreRepository,
        mock_category_repository_with_categories: CategoryRepository,
        horror_genre: Genre,
    ):
        """
        When calling update_genre() with a set of category IDs that do not
        exist in the repository, it raises a RelatedCategoriesNotFound exception.

        This test verifies that the `update_genre` use case raises a
        `RelatedCategoriesNotFound` exception when the given category IDs do not exist
        in the repository.
        """
        use_case = UpdateGenre(
            genre_repository=mock_genre_repository,
            category_repository=mock_category_repository_with_categories,
        )
        mock_genre_repository.get_by_id.return_value = horror_genre  # type: ignore
        with pytest.raises(
            RelatedCategoriesNotFound,
            match="Categories with provided IDs not found: .*",
        ):
            use_case.execute(
                input=UpdateGenre.Input(
                    id=horror_genre.id,
                    name=horror_genre.name,
                    is_active=True,
                    categories={uuid.uuid4()},
                )
            )

        mock_genre_repository.update.assert_not_called()  # type: ignore

    def test_update_genre_with_valid_input(
        self,
        mock_genre_repository: GenreRepository,
        mock_category_repository_with_categories: CategoryRepository,
        genre_id: uuid.UUID,
        horror_genre: Genre,
        movie_category: Category,
        documentary_category: Category,
    ):
        """
        When calling update_genre() with a valid Genre, it updates the genre in
        the repository and returns the updated Genre.

        This test verifies that the `update_genre` use case updates the genre in
        the repository and returns the updated Genre.
        """
        mock_genre_repository.get_by_id.return_value = horror_genre  # type: ignore
        use_case = UpdateGenre(
            genre_repository=mock_genre_repository,
            category_repository=mock_category_repository_with_categories,
        )
        result = use_case.execute(
            input=UpdateGenre.Input(
                id=genre_id,
                name="Horror Updated",
                is_active=False,
                categories={
                    movie_category.id,
                    documentary_category.id,
                },
            )
        )

        assert result == UpdateGenre.Output(
            id=genre_id,
            name="Horror Updated",
            is_active=False,
            categories={
                movie_category.id,
                documentary_category.id,
            },
        )
