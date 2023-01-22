"""voucher URL Configuration."""

from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from voucher_api import views

router = routers.DefaultRouter()
router.register('customers', views.CustomerViewset)


urlpatterns = [
    path('api/v1/oauth2/', include('django_auth_adfs.urls', 'django_auth_adfs')),
    path('api/v1/oauth2/', include('django_auth_adfs.drf_urls', 'django_auth_adfs')),
    path('api/v1/auth/token/', include('rest_framework.urls')),
    path('api/v1/', include(router.urls)),
    path('admin/v1/', admin.site.urls),
]
