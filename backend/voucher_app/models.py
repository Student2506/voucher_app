"""Models to describe subject."""
import logging
import re
from typing import Any

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _

from voucher_app.mixins import TimeStampedMixin, UUIDMixin

TEXT_FIELD_LEN = 255
REPRESENTATION_LEN = 60

logger = logging.getLogger(__name__)


class Template(UUIDMixin, TimeStampedMixin):
    """Model to describe template."""

    title = models.CharField(_('title'), max_length=TEXT_FIELD_LEN, unique=True)
    template_content = models.TextField(_('template_content'), blank=True)
    logo_image = models.FileField(_('logo'), upload_to='uploads/', blank=True, null=True)
    voucher_image = models.FileField(_('voucher_image'), upload_to='uploads/', blank=True, null=True)

    class Meta:
        """Generic Meta class."""

        verbose_name = _('Template')
        verbose_name_plural = _('Templates')
        ordering = ['title']
        db_table = 'voucher_app"."template'

    def clean_template_content(self) -> str:
        """Remove multiple br tags from text.

        Returns:
            str - content
        """
        return str(self.cleaned_data['template_content'].replace('<br />', ''))

    def __str__(self) -> str:
        """Present model as a title.

        Returns:
            str - title of model
        """
        return str(self.title)[:REPRESENTATION_LEN]

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Save data.

        Args:
            args: list[Any] - Any data
            kwargs: dict[Any, Any] - Any data
        """
        super().save(*args, **kwargs)
        for property_name in self.properties.all():
            logger.debug(property_name)


class TemplateProperty(models.Model):
    """Class to describe properties of Template."""

    template = models.ForeignKey('Template', on_delete=models.CASCADE, related_name='properties')
    property_name = models.CharField(_('Property name'), max_length=REPRESENTATION_LEN)
    # property_value = models.TextField(_('Property value'))
    property_locale = models.CharField(_('Template part'), max_length=REPRESENTATION_LEN)

    class Meta:
        """General Meta class."""

        verbose_name = _('TemplateProperty')
        verbose_name_plural = _('TemplateProperties')
        ordering = ['pk']

    def __str__(self) -> str:
        """Represent str.

        Returns:
            str - data to reprsent
        """
        return f'{self.property_name}: {self.property_value[:30]}'

    def __repr__(self) -> str:
        """Represent str.

        Returns:
            str - data to reprsent
        """
        return f'{self.property_name}'

    def save(self, *args: list[Any], **kwargs: dict[Any]) -> None:
        """Save data.

        Args:
            args: list[Any] - Any data
            kwargs: dict[Any, Any] - Any data
        """
        tag_to_find = re.compile(
            r'(\{\% block (' + self.property_name + r') \%\})(.*)(\{\% endblock \2 \%\})',
            flags=re.DOTALL,
        )
        self.template.template_content = re.sub(
            tag_to_find,
            r'\1 ' + self.property_value + r' \4',
            self.template.template_content,
        )
        self.template.save()
        super().save(*args, **kwargs)

    @property
    def propety_value(self) -> str:
        logger.debug('++++++++++++++++++++++++++++++++++')
        tag_to_find = re.compile(
            r'(\{\% block (' + self.property_name + r') \%\})(.*)(\{\% endblock \2 \%\})',
            flags=re.DOTALL,
        )
        result = re.search(tag_to_find, self.template.template_content)
        return str(result.group(3)) if result else ' '


class RequestOrder(UUIDMixin, TimeStampedMixin):
    """Model to get data from user."""

    template = models.ForeignKey('Template', on_delete=models.CASCADE)
    order_item = models.IntegerField()
    addresses = ArrayField(models.EmailField(blank=False, null=False), default=list)
    request_id = models.CharField(_('Request ID'), max_length=TEXT_FIELD_LEN)
    username = models.CharField(_('username'), max_length=TEXT_FIELD_LEN)

    class Meta:
        """Generic Meta class."""

        verbose_name = _('RequestOrder')
        verbose_name_plural = _('RequestOrders')
        ordering = ['id']
        db_table = 'voucher_app"."request_order'
