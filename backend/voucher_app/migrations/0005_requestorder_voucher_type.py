# Generated by Django 4.1.5 on 2023-01-23 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voucher_app', '0004_remove_requestorder_voucher_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestorder',
            name='voucher_type',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]