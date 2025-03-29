from django.contrib import admin

from src.django_project.cast_member_app.models import CastMember


class CastMemberAdmin(admin.ModelAdmin):
    """
    Admin configuration for the CastMember model
    """


admin.site.register(
    CastMember,
    CastMemberAdmin,
)
