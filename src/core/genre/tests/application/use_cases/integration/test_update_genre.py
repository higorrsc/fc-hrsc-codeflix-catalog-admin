import uuid

import pytest

from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
)
from src.core.genre.application.exceptions import (
    GenreNotFound,
    InvalidGenre,
    RelatedCategoriesNotFound,
)
from src.core.genre.application.use_cases.update_genre import UpdateGenre
from src.core.genre.domain.genre import Genre
from src.core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository


class TestUpdateGenre:
    """
    Test class for the `update_genre` use case.
    """

    def test_update_not_existing_genre_raises_exception(self):
        """
        When calling update_genre() with a non-existent genre ID, it raises a
        GenreNotFound exception.

        This test verifies that the `update_genre` use case raises a
        GenreNotFound exception when the genre is not found in the repository.
        """

        use_case = UpdateGenre(
            genre_repository=InMemoryGenreRepository(),
            category_repository=InMemoryCategoryRepository(),
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

    def test_update_genre_with_invalid_input_raises_exception(self):
        """
        When calling update_genre() with an invalid Genre (e.g. with an empty name),
        it raises an InvalidGenre exception.

        This test verifies that the `update_genre` use case raises an
        `InvalidGenre` exception when the given Genre is invalid.
        """

        genre_id = uuid.uuid4()
        use_case = UpdateGenre(
            genre_repository=InMemoryGenreRepository(
                genres=[
                    Genre(
                        id=genre_id,
                        name="Horror",
                    )
                ]
            ),
            category_repository=InMemoryCategoryRepository(),
        )
        with pytest.raises(InvalidGenre, match="Name cannot be empty"):
            use_case.execute(
                input=UpdateGenre.Input(
                    id=genre_id,
                    name="",
                    is_active=False,
                    categories=set(),
                )
            )

    def test_update_genre_with_invalid_related_categories_raises_exception(self):
        """
        When calling update_genre() with a set of category IDs that do not
        exist in the repository, it raises a RelatedCategoriesNotFound exception.

        This test verifies that the `update_genre` use case raises a
        `RelatedCategoriesNotFound` exception when the given category IDs do not exist
        in the repository.
        """

        genre_id = uuid.uuid4()
        use_case = UpdateGenre(
            genre_repository=InMemoryGenreRepository(
                genres=[
                    Genre(
                        id=genre_id,
                        name="Horror",
                    )
                ]
            ),
            category_repository=InMemoryCategoryRepository(categories=[]),
        )

        with pytest.raises(
            RelatedCategoriesNotFound,
            match="Categories with provided IDs not found: .*",
        ):
            use_case.execute(
                input=UpdateGenre.Input(
                    id=genre_id,
                    name="Horror",
                    is_active=True,
                    categories={uuid.uuid4()},
                )
            )

    def test_update_genre_with_valid_input(self):
        """
        When calling update_genre() with a valid Genre, it updates the genre in
        the repository and returns the updated Genre.

        This test verifies that the `update_genre` use case updates the genre in
        the repository and returns the updated Genre.
        """
        movie_category = Category(
            name="Movie",
            description="Movies category",
        )
        documentary_category = Category(
            name="Documentary",
            description="Documentary category",
        )
        cartoon_category = Category(
            name="Cartoon",
            description="Cartoon category",
        )

        genre_id = uuid.uuid4()

        use_case = UpdateGenre(
            genre_repository=InMemoryGenreRepository(
                genres=[
                    Genre(
                        id=genre_id,
                        name="Horror",
                        is_active=True,
                        categories={
                            cartoon_category.id,
                            documentary_category.id,
                        },
                    )
                ]
            ),
            category_repository=InMemoryCategoryRepository(
                [
                    cartoon_category,
                    documentary_category,
                    movie_category,
                ]
            ),
        )
        result = use_case.execute(
            input=UpdateGenre.Input(
                id=genre_id,
                name="Horror Updated",
                is_active=False,
                categories={movie_category.id},
            )
        )

        assert result.id == genre_id
        assert result.name == "Horror Updated"
        assert result.is_active is False
        assert result.categories == {movie_category.id}
