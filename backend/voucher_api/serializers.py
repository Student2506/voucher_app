"""Describe serializers."""

from rest_framework import serializers

from vista_module.models import Customer, Order, OrderItem, VoucherType
from voucher_app.models import RequestOrder, Template


class VoucherTypeSerializer(serializers.ModelSerializer):
    """Voucher type serializer."""

    class Meta:
        """Regular django Meta for Voucher Type."""

        model = VoucherType
        fields = '__all__'


class VoucherTypeOrderingSerializer(VoucherTypeSerializer):
    """Extend VoucherType serializer with fields to make order."""

    templates = serializers.SerializerMethodField()

    def get_templates(self, source: object) -> dict[str, str]:
        """Return dict of templates.

        Args:
            source: object - additional inheritance

        Returns:
            dict - dict with Templates
        """
        return {str(template.id): template.title for template in Template.objects.all()}

    class Meta:
        """Regular django Meta class for Voucher Order."""

        model = VoucherType
        fields = '__all__'


class RequestOrderSerializer(serializers.ModelSerializer):
    """Getting all data to confirm order."""

    class Meta:
        """Meta class for RequestOrder."""

        model = RequestOrder
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    """Order item serializer."""

    voucher_attached = VoucherTypeSerializer(read_only=True)

    class Meta:
        """Regular django Meta."""

        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    """Order serializer."""

    order_items = OrderItemSerializer(many=True, read_only=True)

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
