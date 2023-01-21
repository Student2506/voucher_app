"""Describe serializers."""

from rest_framework import serializers

from vista_module.models import Customer, Order


class OrderSerializer(serializers.ModelSerializer):
    """Order serializer."""

    class Meta:
        """Regular django Meta."""

        model = Order
        fields = '__all__'


class CustomerListSerializer(serializers.ModelSerializer):
    """Customer List serializer."""

    class Meta:
        """Regular django Meta."""

        model = Customer
        fields = '__all__'


class CustomerDetailSerializer(CustomerListSerializer):
    """Customer Detail serializer."""

    orders = OrderSerializer(many=True, read_only=True)
