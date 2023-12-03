from django.db import models
from django.conf import settings


class AuditableModel(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="created", editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="modified", editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)


    class Meta:
        abstract = True