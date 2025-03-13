import uuid
from dataclasses import dataclass, field

from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.application.exceptions import (
    GenreNotFound,
    InvalidGenre,
    RelatedCategoriesNotFound,
)
from src.core.genre.domain.genre_repository import GenreRepository


class UpdateGenre:
    """
    Update a genre in the repository.
    """

    def __init__(
        self,
        genre_repository: GenreRepository,
        category_repository: CategoryRepository,
    ):
        """
        Initialize the UpdateGenre use case.

        Args:
            genre_repository (GenreRepository): The genre repository.
            category_repository (CategoryRepository): The category repository.
        """
        self.genre_repository = genre_repository
        self.category_repository = category_repository

    @dataclass
    class Input:
        """
        Input for the UpdateGenre use case.
        """

        id: uuid.UUID
        name: str
        is_active: bool
        categories: set[uuid.UUID] = field(default_factory=set)

    @dataclass
    class Output:
        """
        Output for the UpdateGenre use case.
        """

        id: uuid.UUID
        name: str
        is_active: bool
        categories: set[uuid.UUID]

    def execute(self, input: Input) -> Output:
        """
        Execute the UpdateGenre use case.

        Args:
            input (Input): The input for the use case.

        Returns:
            Output: The output of the use case.
        """
        genre = self.genre_repository.get_by_id(genre_id=input.id)

        if genre is None:
            raise GenreNotFound(f"Genre with ID {input.id} not found")

        current_name = genre.name

        categories = {category.id for category in self.category_repository.list()}
        if not input.categories.issubset(categories):
            raise RelatedCategoriesNotFound(
                f"Categories with provided IDs not found: {input.categories - categories}"
            )

        try:
            if input.name is not None:
                current_name = input.name

            genre.change_name(current_name)

            if input.is_active is True:
                genre.activate()

            if input.is_active is False:
                genre.deactivate()

            genre.categories = input.categories

        except ValueError as err:
            raise InvalidGenre(err) from err

        self.genre_repository.update(genre)

        return self.Output(
            id=genre.id,
            name=genre.name,
            is_active=genre.is_active,
            categories=genre.categories,
        )
