import uuid

from django.db import models

from src.core.cast_member.domain.cast_member import CastMemberType


# Create your models here.
class CastMember(models.Model):
    app_label = "cast_member_app"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, null=False, blank=False)
    type = models.CharField(
        max_length=8,
        null=False,
        blank=False,
        choices=[(tag.name, tag.value) for tag in CastMemberType],
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Cast Member"
        verbose_name_plural = "Cast Members"
        db_table = "cast_member"
