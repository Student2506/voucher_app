"""General model for admin."""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from voucher_app.models import Template

admin.site.site_title = _('My site name')
admin.site.site_header = _('My site header')
admin.site.index_title = _('My index title')


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    """General class ot work with model."""

    pass
