import uuid
from dataclasses import dataclass, field

from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.application.exceptions import (
    InvalidGenre,
    RelatedCategoriesNotFound,
)
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository


class CreateGenre:
    """
    Create a new genre with the given name and categories.
    """

    def __init__(
        self,
        genre_repository: GenreRepository,
        category_repository: CategoryRepository,
    ):
        """
        Initialize the CreateGenre use case.

        Args:
            genre_repository (GenreRepository): The genre repository.
            category_repository (CategoryRepository): The category repository.
        """
        self.genre_repository = genre_repository
        self.category_repository = category_repository

    @dataclass
    class Input:
        """
        Input for the CreateGenre use case.
        """

        name: str
        is_active: bool = True
        categories: set[uuid.UUID] = field(default_factory=set)

    @dataclass
    class Output:
        """
        Output for the CreateGenre use case.
        """

        id: uuid.UUID

    def execute(self, input: Input) -> Output:
        """
        Create a new genre with the given name and categories.

        Args:
            input (CreateGenre.Input): The input for the CreateGenre use case.

        Returns:
            CreateGenre.Output: The output of the CreateGenre use case, containing the ID
                of the newly created genre.

        Raises:
            RelatedCategoriesNotFound: If the input includes categories that are not
                found in the category repository.
        """
        categories = {category.id for category in self.category_repository.list()}
        if not input.categories.issubset(categories):
            raise RelatedCategoriesNotFound(
                f"Categories with provided IDs not found: {input.categories - categories}"
            )

        try:
            genre = Genre(
                name=input.name,
                is_active=input.is_active,
                categories=input.categories,
            )
        except ValueError as err:
            raise InvalidGenre(err) from err

        self.genre_repository.save(genre)
        return self.Output(id=genre.id)
