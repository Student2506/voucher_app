from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contragent/<int:company>', views.voucher_index, name='voucher'),
    path('voucher/<int:voucher>', views.codes_index, name='codes'),
]
