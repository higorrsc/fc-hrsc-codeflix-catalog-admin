from django.contrib import admin

from src.django_project.genre_app.models import Genre


class GenreAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Genre model
    """


admin.site.register(
    Genre,
    GenreAdmin,
)
