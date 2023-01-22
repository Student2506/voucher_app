"""Describe serializers."""

from rest_framework import serializers

from vista_module.models import Customer, Order, OrderItem, VoucherType
from voucher_app.models import Template


class VoucherTypeSerializer(serializers.ModelSerializer):
    """Voucher type serializer."""

    email_templates = serializers.SerializerMethodField()
    example_email = serializers.SerializerMethodField()

    def get_email_templates(self, instance: object) -> dict[str, str]:
        """Get templates list.

        Args:
            instance: object - instance to act upon

        Returns:
            dict[str, str] - returns json with template
        """
        return {str(template.id): template.title for template in Template.objects.all()}

    def get_example_email(self, instance: object) -> str:
        """Get user email.

        Args:
            instance: object - instance to act upon

        Returns:
            str - returns user email as example
        """
        request = self.context.get('request', None)
        if request:
            return str(request.user.email)
        return ''

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
