"""voucher URL Configuration."""

from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from voucher_api import views

router = routers.DefaultRouter()
router.register('customers', views.CustomerViewset)


urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('admin/v1/', admin.site.urls),
]
