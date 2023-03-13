"""Describe serializers."""
import logging
from typing import Any

from rest_framework import serializers
from voucher_app.models import RequestOrder, Template

from vista_module.models import Customer, Order, OrderItem, VoucherType

logger = logging.getLogger(__name__)


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
        return {
            str(template.id): template.title
            for template in Template.objects.all()
        }

    def to_representation(
        self,
        instance: Any,
    ) -> Any:
        """Cut whitespaces in the end.

        Args:
            instance: Any - instance of serializer

        Returns:
            Any - instance of serializer

        Raise:
            TypeError
        """
        ret = super().to_representation(instance)
        raise TypeError(instance)
        ret['voucher_description'] = ret['voucher_description'].rtrim() # noqa: WPS427, E501
        return ret  # noqa: WPS427

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
