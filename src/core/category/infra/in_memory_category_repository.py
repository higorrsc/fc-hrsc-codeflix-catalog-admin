from src.core.category.application.category_repository import CategoryRepository


class InMemoryCategoryRepository(CategoryRepository):
    """
    In memory category repository
    """

    def __init__(self, categories=None):
        """
        Initialize the in-memory category repository.

        Args:
            categories (list, optional): A list of categories to initialize the repository with.
            Defaults to an empty list if not provided.
        """
        self.categories = categories or []

    def save(self, category):
        """
        Save a category to the in-memory repository.

        Args:
            category (Category): The category to be saved.
        """
        self.categories.append(category)
