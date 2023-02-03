"""File describing mixin for other modules."""
import uuid

from django.db import models


class TimeStampedMixin(models.Model):
    """Mixin for standard datetime fileds."""

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        """Generic Meta class."""

        abstract = True


class UUIDMixin(models.Model):
    """Mixin to add uuid field."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        """Generic Meta class."""

        abstract = True
