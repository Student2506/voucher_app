"""Module for admin."""

from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """General class to handle admin interface."""

    pass
