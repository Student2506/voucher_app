"""Module to descibe VISTA."""

from django.db import models

NAME_LENGTH = 50
ORDER_NAME_LENGTH = 100


class Customer(models.Model):
    """Customer model."""

    sname = models.CharField(
        verbose_name='Наименование организации',
        db_column='sName',
        max_length=NAME_LENGTH,
        blank=False,
        null=False,
    )
    id = models.IntegerField(db_column='lID', primary_key=True)

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

    id = models.IntegerField(db_column='lID', primary_key=True)
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
        """Return represntation.

        Returns:
            str - name of a customer
        """
        return str(self.name[:NAME_LENGTH])
