"""General vista api app config."""

from django.apps import AppConfig


class VoucherApiConfig(AppConfig):
    """Generic app config."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'voucher_api'
