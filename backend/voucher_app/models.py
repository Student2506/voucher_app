"""Models to describe subject."""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

TEXT_FIELD_LEN = 255


class User(AbstractUser):
    """Stub to describe user."""

    pass


class Template(models.Model):
    """Model to describe template."""

    title = models.CharField(_('title'), max_length=TEXT_FIELD_LEN)
    template_content = models.TextField(_('template_content'), blank=True)

    class Meta:
        """Generic Meta class."""

        verbose_name = _('Template')
        verbose_name_plural = _('Templates')
        ordering = ['title']
