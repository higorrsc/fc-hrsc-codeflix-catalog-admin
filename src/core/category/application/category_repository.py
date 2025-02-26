from abc import ABC, abstractmethod


class CategoryRepository(ABC):
    """
    Interface for a category repository.
    """

    @abstractmethod
    def save(self, category):
        """
        Save a category to the repository.

        Args:
            category (Category): The category to be saved.
        """
        raise NotImplementedError
