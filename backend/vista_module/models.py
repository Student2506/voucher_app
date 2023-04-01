"""Module to descibe VISTA."""

from django.db import models

NAME_LENGTH = 50
ORDER_NAME_LENGTH = 100
VOUCHER_TYPE_LENGTH = 30
ID_COLUMN_NAME = 'lID'


class Customer(models.Model):
    """Customer model."""

    customer_name = models.CharField(
        verbose_name='Наименование организации',
        db_column='sName',
        max_length=NAME_LENGTH,
        blank=False,
        null=False,
    )
    customer_id = models.IntegerField(
        db_column=ID_COLUMN_NAME,
        primary_key=True,
    )

    class Meta:
        """Generic Meta class."""

        managed = False
        db_table = 'tblClient'
        ordering = ['customer_name']

    def __str__(self) -> str:
        """Return represntation.

        Returns:
            str - name of a customer
        """
        return str(self.customer_name[:NAME_LENGTH])


class Order(models.Model):
    """Order model."""

    order_id = models.IntegerField(db_column=ID_COLUMN_NAME, primary_key=True)
    order_name = models.CharField(
        verbose_name='Наименование заказа',
        db_column='ClientOrder_strName',
        max_length=ORDER_NAME_LENGTH,
        blank=False,
        null=False,
    )
    client_ref = models.ForeignKey(
        'Customer',
        on_delete=models.DO_NOTHING,
        db_column='lClientID',
        related_name='orders',
    )
    order_date = models.DateTimeField(
        db_column='dOrderedDate',
        verbose_name='Дата-время заказа',
        blank=False,
        null=False,
    )

    class Meta:
        """Generic Meta class."""

        managed = False
        db_table = 'tblClientOrder'
        ordering = ['-order_date', 'order_id']

    def __str__(self) -> str:
        """Return represntation of order.

        Returns:
            str - name of a customer
        """
        return str(self.order_name[:NAME_LENGTH])


class VoucherType(models.Model):
    """Voucher model."""

    voucher_type_id = models.IntegerField(
        db_column=ID_COLUMN_NAME,
        primary_key=True,
    )
    voucher_code = models.CharField(
        db_column='nVoucherCode',
        max_length=VOUCHER_TYPE_LENGTH,
    )
    voucher_description = models.CharField(
        db_column='sDescription',
        max_length=NAME_LENGTH,
    )
    vouchertype_strgiftcard = models.CharField(
        db_column='VoucherType_strGiftCard', max_length=1,
    )

    class Meta:
        """Generic Meta class for VoucherType."""

        managed = False
        db_table = 'tblVoucherType'
        ordering = ['voucher_description']

    def __str__(self) -> str:
        """Return represntation of voucher type.

        Returns:
            str - name of a customer
        """
        return f'{self.voucher_description} - {self.voucher_code}'


class OrderItem(models.Model):
    """Order item model."""

    order_item_id = models.IntegerField(
        db_column=ID_COLUMN_NAME, primary_key=True
    )
    order_id = models.ForeignKey(
        'Order',
        on_delete=models.DO_NOTHING,
        db_column='lClientOrderID',
        related_name='order_items',
    )
    order_item_quantity = models.IntegerField(db_column='lQtyOrdered')
    order_item_price = models.FloatField(db_column='mIssuePrice')
    voucher_attached = models.OneToOneField(
        'VoucherType',
        on_delete=models.DO_NOTHING,
        db_column='lVoucherTypeID',
        related_name='voucher_items',
    )

    class Meta:
        """Generic Meta class."""

        managed = False
        db_table = 'tblClientOrderItem'
        ordering = ['order_item_id']

    def __str__(self) -> str:
        """Return represntation of order's item.

        Returns:
            str - name of a customer
        """
        return f'{self.order_id.order_name} - {self.order_item_id}'


class Stock(models.Model):
    """Stock Model."""

    voucher_number = models.IntegerField(db_column='lVoucherNumber', primary_key=True)
    voucher_type_id = models.ForeignKey(
        'VoucherType',
        on_delete=models.DO_NOTHING,
        db_column='lVoucherTypeID',
        related_name='order_items',
    )
    stock_strbarcode = models.CharField(db_column='Stock_strBarcode', max_length=NAME_LENGTH)
    expiry_date = models.CharField(db_column='dExpiryDate')
    issued_date = models.CharField(db_column='dIssuedDate')
    client_order_item = models.ForeignKey(
        'OrderItem',
        on_delete=models.DO_NOTHING,
        db_column='lClientOrderItemID',
        related_name='order_item_id_set'
    )

    class Meta:
        """Generic Meta class."""

        managed = False
        db_table = 'tblStock'
        ordering = ['voucher_number']
