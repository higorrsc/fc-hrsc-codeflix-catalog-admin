import uuid
from typing import List

from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.django_project.category_app.models import Category as CategoryModel


class DjangoORMCategoryRepository(CategoryRepository):
    """
    Django ORM implementation for a category repository.
    """

    def __init__(self, category_model: CategoryModel | None = None):
        """
        Initialize the DjangoORMCategoryRepository with an optional CategoryModel.

        Args:
            category_model (CategoryModel | None): An optional CategoryModel instance.
                If not provided, the default CategoryModel is used.
        """

        self.category_model = category_model or CategoryModel

    def save(self, category: Category):
        """
        Save a category to the Django ORM database.

        Args:
            category (Category): The category to be saved.
        """

        category_model = CategoryModelMapper.to_model(category)
        category_model.save()

    def get_by_id(self, category_id: uuid.UUID) -> Category | None:
        """
        Retrieve a category by its ID from the Django ORM database.

        Args:
            category_id (uuid.UUID): The ID of the category to be retrieved.

        Returns:
            Category | None: The category with the given ID, or None if it doesn't exist.
        """

        try:
            category = self.category_model.objects.get(pk=category_id)
            return CategoryModelMapper.to_entity(category)
        except self.category_model.DoesNotExist:
            return None

    def delete(self, category_id: uuid.UUID):
        """
        Delete a category by its ID from the Django ORM database.

        Args:
            category_id (uuid.UUID): The ID of the category to be deleted.
        """

        self.category_model.objects.filter(pk=category_id).delete()

    def update(self, category: Category):
        """
        Update a category in the Django ORM database.

        Args:
            category (Category): The category to be updated.

        Raises:
            ValueError: If the category ID does not exist in the database.
        """

        category_data = {
            "name": category.name,
            "description": category.description,
            "is_active": category.is_active,
        }

        self.category_model.objects.filter(pk=category.id).update(**category_data)

    def list(self) -> List[Category]:
        """
        List all categories from the Django ORM database.

        Returns:
            list[Category]: A list of all categories in the database.
        """

        return [
            CategoryModelMapper.to_entity(category_model)
            for category_model in self.category_model.objects.all()
        ]


class CategoryModelMapper:
    """
    A class for mapping between Category and CategoryModel.
    """

    @staticmethod
    def to_model(category: Category) -> CategoryModel:
        """
        Maps a Category entity to a CategoryModel.

        Args:
            category (Category): The category entity to be mapped.

        Returns:
            CategoryModel: The mapped CategoryModel.
        """

        return CategoryModel(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active,
        )

    @staticmethod
    def to_entity(category_model: CategoryModel) -> Category:
        """
        Maps a CategoryModel to a Category entity.

        Args:
            category_model (CategoryModel): The category model to be mapped.

        Returns:
            Category: The mapped Category entity.
        """

        return Category(
            id=category_model.id,
            name=category_model.name,
            description=category_model.description,  # type: ignore
            is_active=category_model.is_active,
        )
