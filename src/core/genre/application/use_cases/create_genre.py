import uuid
from dataclasses import dataclass, field

from src.core.genre.application.exceptions import (
    InvalidGenre,
    RelatedCategoriesNotFound,
)
from src.core.genre.domain.genre import Genre


class CreateGenre:
    def __init__(
        self,
        genre_repository,
        category_repository,
    ):
        self.genre_repository = genre_repository
        self.category_repository = category_repository

    @dataclass
    class Input:
        """
        Input for the CreateGenre use case.
        """

        name: str
        category_ids: set[uuid.UUID] = field(default_factory=set)
        is_active: bool = True

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
        category_ids = {category.id for category in self.category_repository.list()}
        if not input.category_ids.issubset(category_ids):
            raise RelatedCategoriesNotFound(
                f"Categories not found: {input.category_ids - category_ids}"
            )

        try:
            genre = Genre(
                name=input.name,
                is_active=input.is_active,
                categories=input.category_ids,
            )
        except ValueError as err:
            raise InvalidGenre(err) from err

        self.genre_repository.save(genre)
        return self.Output(id=genre.id)
