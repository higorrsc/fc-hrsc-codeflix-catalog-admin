import uuid

from django.db import models


# Create your models here.
class Category(models.Model):
    """
    Category model
    """

    app_label = "category_app"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        """
        Meta class for the Category model.
        """

        verbose_name = "Category"
        verbose_name_plural = "Categories"
        db_table = "category"
