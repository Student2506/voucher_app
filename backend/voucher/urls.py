"""voucher URL Configuration."""

from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from rest_framework.schemas import get_schema_view

from voucher_api import views

router = routers.DefaultRouter()
router.register('customers', views.CustomerViewset)
router.register('voucher_type', views.VoucherTypeViewset)
router.register('order_item', views.OrderItemViewset)


urlpatterns = [
    path(
        'api/v1/oauth2/',
        include('django_auth_adfs.urls', 'django_auth_adfs'),
    ),
    path(
        'api/v1/oauth2/',
        include('django_auth_adfs.drf_urls', 'django_auth_adfs'),
    ),
    path('api/v1/retrieve-token', views.retrieve_token, name='retrieve-token'),
    path('api/v1/clear-session', views.clear_session, name='clear-session'),
    path('api/v1/auth/', include('djoser.urls')),
    path('api/v1/auth/', include('djoser.urls.jwt')),
    path('api/v1/', include(router.urls)),
    path(
        'api/v1/order_item/<int:order_item_id>/',
        views.put_order,
        name='order-detail',
    ),
    path('admin/v1/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
    path(
        'openapi',
        get_schema_view(
            title='Voucher API',
            description='API for voucher generation',
            version='1.0.0',
        ),
        name='openapi-schema',
    ),
]
