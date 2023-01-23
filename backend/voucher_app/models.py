"""Models to describe subject."""
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _

from voucher_app.mixins import TimeStampedMixin, UUIDMixin

TEXT_FIELD_LEN = 255
REPRESENTATION_LEN = 30


class Template(UUIDMixin, TimeStampedMixin):
    """Model to describe template."""

    title = models.CharField(_('title'), max_length=TEXT_FIELD_LEN, unique=True)
    template_content = models.TextField(_('template_content'), blank=True)

    class Meta:
        """Generic Meta class."""

        verbose_name = _('Template')
        verbose_name_plural = _('Templates')
        ordering = ['title']
        db_table = 'voucher_app"."template'

    def __str__(self) -> str:
        """Present model as a title.

        Returns:
            str - title of model
        """
        return str(self.title)[:REPRESENTATION_LEN]


class RequestOrder(UUIDMixin, TimeStampedMixin):
    """Model to get data from user."""

    template = models.ForeignKey('Template', on_delete=models.CASCADE)
    order_item = models.IntegerField()
    addresses = ArrayField(models.EmailField(blank=False, null=False), default=list)

    class Meta:
        """Generic Meta class."""

        verbose_name = _('RequestOrder')
        verbose_name_plural = _('RequestOrders')
        ordering = ['id']
        db_table = 'voucher_app"."request_order'
