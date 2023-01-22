"""Views to serve vista objects."""

from rest_framework import serializers, viewsets

from vista_module.models import Customer
from voucher_api.serializers import (
    CustomerDetailSerializer,
    CustomerListSerializer,
)


class CustomerViewset(viewsets.ReadOnlyModelViewSet):
    """API Endpoint which allows to view Customers."""

    queryset = Customer.objects.using('vista')

    def get_serializer_class(self) -> serializers.ModelSerializer:
        """Choose serializer.

        Returns:
            serializers.ModelSerializer - instance to use
        """
        if self.action == 'retrieve':
            return CustomerDetailSerializer
        return CustomerListSerializer
