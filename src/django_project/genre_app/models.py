import uuid

from django.db import models


# Create your models here.
class Genre(models.Model):
    app_label = "genre_app"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, null=False, blank=False)
    categories = models.ManyToManyField(
        to="category_app.Category",
        related_name="genres",
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"
        db_table = "genre"
