"""Module to descibe VISTA."""

from django.db import models

NAME_LENGTH = 50
ORDER_NAME_LENGTH = 100
VOUCHER_TYPE_LENGTH = 30
ID_COLUMN_NAME = 'lID'


class Customer(models.Model):
    """Customer model."""

    name = models.CharField(
        verbose_name='Наименование организации',
        db_column='sName',
        max_length=NAME_LENGTH,
        blank=False,
        null=False,
    )
    id = models.IntegerField(db_column=ID_COLUMN_NAME, primary_key=True)

    class Meta:
        """Generic Meta class."""

        managed = False
        db_table = 'tblClient'

    def __str__(self) -> str:
        """Return represntation.

        Returns:
            str - name of a customer
        """
        return str(self.sname[:NAME_LENGTH])


class Order(models.Model):
    """Order model."""

    id = models.IntegerField(db_column=ID_COLUMN_NAME, primary_key=True)
    name = models.CharField(
        verbose_name='Наименование заказа',
        db_column='ClientOrder_strName',
        max_length=ORDER_NAME_LENGTH,
        blank=False,
        null=False,
    )
    client = models.ForeignKey(
        'Customer',
        on_delete=models.DO_NOTHING,
        db_column='lClientID',
        related_name='orders',
    )

    class Meta:
        """Generic Meta class."""

        managed = False
        db_table = 'tblClientOrder'

    def __str__(self) -> str:
        """Return represntation of order.

        Returns:
            str - name of a customer
        """
        return str(self.name[:NAME_LENGTH])


class VoucherType(models.Model):
    """Voucher model."""

    id = models.IntegerField(db_column=ID_COLUMN_NAME, primary_key=True)
    voucher_code = models.CharField(
        db_column='nVoucherCode',
        max_length=VOUCHER_TYPE_LENGTH,
    )
    description = models.CharField(
        db_column='sDescription',
        max_length=NAME_LENGTH,
    )

    class Meta:
        """Generic Meta class for VoucherType."""

        managed = False
        db_table = 'tblVoucherType'

    def __str__(self) -> str:
        """Return represntation of voucher type.

        Returns:
            str - name of a customer
        """
        return f'{self.description} - {self.voucher_code}'


class OrderItem(models.Model):
    """Order item model."""

    id = models.IntegerField(db_column=ID_COLUMN_NAME, primary_key=True)
    order = models.ForeignKey(
        'Order',
        on_delete=models.DO_NOTHING,
        db_column='lClientOrderID',
        related_name='voucher_items',
    )
    quantity = models.IntegerField(db_column='lQtyOrdered')
    price = models.FloatField(db_column='mIssuePrice')
    voucher = models.ForeignKey(
        'VoucherType',
        on_delete=models.DO_NOTHING,
        db_column='lVoucherTypeID',
        related_name='voucher_items',
    )

    class Meta:
        """Generic Meta class."""

        managed = False
        db_table = 'tblClientOrderItem'

    def __str__(self) -> str:
        """Return represntation of order's item.

        Returns:
            str - name of a customer
        """
        return f'{self.order.name} - {self.id}'
