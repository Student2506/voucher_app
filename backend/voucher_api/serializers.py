"""Describe serializers."""
import logging
from typing import Any

from rest_framework import serializers
from voucher_app.models import RequestOrder, Template

from vista_module.models import Customer, Order, OrderItem, Stock, VoucherType

logger = logging.getLogger(__name__)


class VoucherTypeSerializer(serializers.ModelSerializer):
    """Voucher type serializer."""

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
        ret['voucher_description'] = ret['voucher_description'].rstrip()
        return ret  # noqa: WPS427

    class Meta:
        """Regular django Meta for Voucher Type."""

        model = VoucherType
        fields = ['voucher_type_id', 'voucher_code', 'voucher_description']


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
        ret['voucher_description'] = ret['voucher_description'].rstrip()
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


class OrderItemListSerializer(serializers.ModelSerializer):
    """Order item serializer."""

    # voucher_attached = VoucherTypeSerializer(read_only=True)
    voucher_type_id = serializers.IntegerField(source='voucher_attached.voucher_type_id')
    voucher_code = serializers.CharField(source='voucher_attached.voucher_code')
    voucher_description = serializers.CharField(source='voucher_attached.voucher_description')

    class Meta:
        """Regular django Meta."""

        model = OrderItem
        exclude = ('voucher_attached',)

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
        ret['voucher_description'] = ret['voucher_description'].rstrip()
        return ret  # noqa: WPS427


class OrderItemItemSerializer(OrderItemListSerializer):
    """Order item serializer."""

    templates = serializers.SerializerMethodField()

    class Meta:
        """Regular django Meta."""

        model = OrderItem
        exclude = ('voucher_attached',)

    def get_templates(self, source: object) -> dict[str, str]:
        """Return dict of templates.

        Args:
            source: object - additional inheritance

        Returns:
            dict - dict with Templates
        """
        return {str(template.id): template.title for template in Template.objects.all()}


class CustomerListSerializer(serializers.ModelSerializer):
    """Customer List serializer."""

    class Meta:
        """Regular django Meta."""

        model = Customer
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    """Order serializer."""

    order_items = OrderItemListSerializer(many=True, read_only=True)

    class Meta:
        """Regular django Meta."""

        model = Order
        fields = '__all__'


class CustomerDetailSerializer(CustomerListSerializer):
    """Customer Detail serializer."""

    orders = OrderSerializer(many=True, read_only=True)


class StockSerializer(serializers.ModelSerializer):
    """Stock Serializer."""

    order_id = serializers.IntegerField(source='client_order_item.order_id.order_id')

    class Meta:
        """Regular django Meta."""

        model = Stock
        fields = '__all__'


class StockWriteSerializer(serializers.ModelSerializer):
    """Write data to DB."""

    class Meta:
        model = Stock
        fields = ('stock_strbarcode', 'expiry_date')
