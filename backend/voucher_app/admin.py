"""General model for admin."""

from django import forms
from django.contrib import admin
from django.db import models
from django.utils.translation import gettext_lazy as _
from tinymce.widgets import TinyMCE

from voucher_app.models import Template

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


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    """General class ot work with model."""

    form = TemplateAdminForm
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE(mce_attrs=mce_attrs)},
    }
