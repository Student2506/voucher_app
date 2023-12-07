"""Describe serializers."""
import logging
import re
from typing import Any

from rest_framework import serializers

from vista_module.models import (
    Customer,
    Order,
    OrderItem,
    RedeemedCard,
    Stock,
    VoucherType,
)
from voucher_app.models import RequestOrder, Template

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
        return {str(template.id): template.title for template in Template.objects.all()}

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

    voucher_type_id = serializers.IntegerField(
        source='voucher_attached.voucher_type_id',
    )
    voucher_code = serializers.CharField(source='voucher_attached.voucher_code')
    voucher_description = serializers.CharField(
        source='voucher_attached.voucher_description',
    )

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
    order_naming = serializers.CharField(source='order_id.order_naming')

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

    expiry_date = serializers.SerializerMethodField()

    class Meta:
        """Regular django Meta."""

        model = Stock
        fields = [
            'voucher_number',
            'expiry_date',
            'duplicate_no',
            'stock_strbarcode',
            'issued_date',
            'voucher_type_id',
            'client_order_item',
        ]

    def get_expiry_date(self, stock: Stock) -> str:
        """Return date as string.

        Args:
            stock: Stock - whole object of type Stock

        Returns:
            str - date formatted
        """
        return str(stock.expiry_date.strftime('%Y-%m-%d %H:%M:%S'))


class RedeemedSerializer(serializers.ModelSerializer):
    """Redeemed model serializer."""

    class Meta:
        """Regular Meta class."""

        model = RedeemedCard
        fieids = '__all__'


class StockWriteSerializer(serializers.ModelSerializer):
    """Write data to DB."""

    expiry_date = serializers.SerializerMethodField()

    class Meta:
        """Regular Meta class."""

        model = Stock
        fields = ('stock_strbarcode', 'expiry_date')

    def get_expiry_date(self, stock: Stock) -> str:
        """Return date as string.

        Args:
            stock: Stock - whole object of type Stock

        Returns:
            str - date formatted
        """
        return str(stock.expiry_date.strftime('%Y-%m-%d %H:%M:%S'))


class TemplateSerializer(serializers.ModelSerializer):
    """Template Serializer."""

    template_property = serializers.SerializerMethodField()

    class Meta:
        """Regular Meta class."""

        model = Template
        fields = ('id', 'title', 'logo_image', 'voucher_image', 'template_property')

    def get_template_property(self, template: Template) -> list[dict[str, Any]]:
        """Retrieve template property.

        Args:
            template: Template - template to parse

        Returns:
            list[dict[str, Any]] - list of properties
        """
        properties = []
        for prop in template.properties.all():
            tag_to_find = re.compile(
                r'(\{\% block ('
                + prop.property_name
                + r') \%\})(.*)(\{\% endblock \2 \%\})',
                flags=re.DOTALL,
            )
            template_tag = re.search(tag_to_find, template.template_content)
            part = {
                'name': prop.property_name,
                'locale': prop.property_locale,
                'content': template_tag.group(3) if template_tag else None,
            }
            properties.append(part)
        return properties
