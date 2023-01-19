"""Main module for serving application."""

from django.apps import AppConfig


class VoucherAppConfig(AppConfig):
    """Main application."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'voucher_app'
