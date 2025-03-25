import uuid
from dataclasses import dataclass
from typing import Generic, Type, TypeVar

TRepository = TypeVar("TRepository")


@dataclass
class DeleteRequest:
    """
    Represents the request to delete an entity by its ID.
    """

    id: uuid.UUID


class DeleteUseCase(Generic[TRepository]):
    """
    Use case to delete an entity by its ID.
    """

    def __init__(
        self,
        repository: TRepository,
        not_found_exception: Type[Exception],
        not_found_message: str,
    ):
        """
        Initialize the DeleteUseCase.

        Args:
            repository (TRepository): The repository of the entity to be deleted.
            not_found_exception (Type[Exception]): The exception to be raised
                when the entity is not found.
            not_found_message (str): The message to be displayed when the entity is not found.
        """

        self.repository = repository
        self.not_found_exception = not_found_exception
        self.not_found_message = not_found_message

    def execute(self, request: DeleteRequest) -> None:
        """
        Deletes an entity by its ID.

        Args:
            request (DeleteRequest): The request with the ID of the entity to be deleted.

        Raises:
            self.not_found_exception: If the entity is not found.
        """

        entity = self.repository.get_by_id(request.id)  # type: ignore

        if entity is None:
            raise self.not_found_exception(self.not_found_message.format(id=request.id))

        self.repository.delete(request.id)  # type: ignore
