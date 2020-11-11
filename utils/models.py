from django.db import models
from user.models import User


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_created_by',
        blank=True, null=True,
    )
    modified_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_modified_by',
        blank=True, null=True,
    )

    class Meta:
        abstract = True
