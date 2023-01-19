"""File to describe admin."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from voucher_app.models import Template, User


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    """Stub to work with Template model."""

    pass


admin.site.register(User, UserAdmin)
