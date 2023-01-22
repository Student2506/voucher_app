"""Describe serializers."""

from rest_framework import serializers

from vista_module.models import Customer, Order, OrderItem, VoucherType


class VoucherTypeSerializer(serializers.ModelSerializer):
    """Voucher type serializer."""

    class Meta:
        """Regular djange Meta for Voucher Type."""

        model = VoucherType
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    """Order item serializer."""

    voucher = VoucherTypeSerializer(read_only=True)

    class Meta:
        """Regular django Meta."""

        model = OrderItem
        exclude = ('order',)


class OrderSerializer(serializers.ModelSerializer):
    """Order serializer."""

    voucher_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        """Regular django Meta."""

        model = Order
        exclude = ('client',)


class CustomerListSerializer(serializers.ModelSerializer):
    """Customer List serializer."""

    class Meta:
        """Regular django Meta."""

        model = Customer
        fields = '__all__'


class CustomerDetailSerializer(CustomerListSerializer):
    """Customer Detail serializer."""

    orders = OrderSerializer(many=True, read_only=True)
