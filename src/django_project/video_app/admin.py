from django.contrib import admin

from src.django_project.video_app.models import AudioVideoMedia, ImageMedia, Video


class VideoAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Video model
    """


class AudioVideoMediaAdmin(admin.ModelAdmin):
    """
    Admin configuration for the AudioVideoMedia model
    """


class ImageMediaAdmin(admin.ModelAdmin):
    """
    Admin configuration for the ImageMedia model
    """


admin.site.register(
    Video,
    VideoAdmin,
)

admin.site.register(
    AudioVideoMedia,
    AudioVideoMediaAdmin,
)

admin.site.register(
    ImageMedia,
    ImageMediaAdmin,
)
