"""General model for admin."""

from django import forms
from django.contrib import admin
from django.db import models
from django.utils.translation import gettext_lazy as _
from tinymce.widgets import TinyMCE

from voucher_app.models import Template, TemplateProperty

admin.site.site_title = _('My site name')
admin.site.site_header = _('My site header')
admin.site.index_title = _('My index title')

mce_attrs = {
    'protect': [
       '/{%(.*)%}/g',
       '/{{(.*)}}/g',
       '/{#(.*)#}/g',
    ],
    'forced_root_block': '',
}


class TemplateAdminForm(forms.ModelForm):
    """Form to use with cleanup extra tinymce stuff."""

    class Meta:
        """Just regular Meta class."""

        model = Template
        fields = '__all__'

    def clean_template_content(self) -> str:
        """Remove multiple br tags from text.

        Returns:
            str - content
        """
        template_content: str = self.cleaned_data['template_content'].replace('<br />', '')
        return template_content.replace('%}', '%}<br />')


class PropertiesInline(admin.StackedInline):
    """General class to manage properties."""

    model = TemplateProperty
    verbose_name = _('Attribute')
    verbose_name_plural = _('Attributes')
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE(mce_attrs=mce_attrs)},
    }
    fields = ('property_locale', 'property_value')
    extra = 1


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    """General class ot work with model."""

    form = TemplateAdminForm
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE(mce_attrs=mce_attrs)},
    }
    save_as = True
    fieldsets = [
        (
            None,
            {
                'fields': ['title', ('logo_image', 'voucher_image')],
            },
        ),
        (
            _('Advanced options'),
            {
                'classes': ['collapse'],
                'fields': ['template_content'],
            },
        ),
    ]
    list_display = ['title', 'logo_image', 'voucher_image']
    inlines = [PropertiesInline]


@admin.register(TemplateProperty)
class TemplatePropertyAdmin(admin.ModelAdmin):
    """General class."""

    pass
