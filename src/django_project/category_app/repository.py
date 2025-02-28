import uuid
from typing import List

from django_project.category_app.models import Category as CategoryModel
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository


class DjangoORMCategoryRepository(CategoryRepository):
    """
    Django ORM implementation for a category repository.
    """

    def __init__(self, category_model: CategoryModel | None = None):
        self.category_model = category_model or CategoryModel

    def save(self, category: Category):
        category_data = {
            "id": category.id,
            "name": category.name,
            "description": category.description,
            "is_active": category.is_active,
        }

        self.category_model.objects.create(**category_data)

    def get_by_id(self, category_id: uuid.UUID) -> Category | None:
        try:
            category = self.category_model.objects.get(pk=category_id)
            return Category(
                id=category.id,
                name=category.name,
                description=category.description,
                is_active=category.is_active,
            )
        except self.category_model.DoesNotExist:
            return None

    def delete(self, category_id: uuid.UUID):
        self.category_model.objects.filter(pk=category_id).delete()

    def update(self, category: Category):
        category_data = {
            "name": category.name,
            "description": category.description,
            "is_active": category.is_active,
        }

        self.category_model.objects.filter(pk=category.id).update(**category_data)

    def list(self) -> List[Category]:
        return [
            Category(
                id=category.id,
                name=category.name,
                description=category.description,
                is_active=category.is_active,
            )
            for category in self.category_model.objects.all()
        ]
