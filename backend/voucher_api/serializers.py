"""Describe serializers."""

from rest_framework import serializers

from vista_module.models import Customer, Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    """Order item serializer."""

    class Meta:
        """Regular django Meta."""

        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    """Order serializer."""

    voucher_items = OrderItemSerializer(many=True, read_only=True)

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
