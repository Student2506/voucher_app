# Generated by Django 4.1.5 on 2023-06-01 09:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("voucher_app", "0003_alter_templateproperty_property_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="template",
            name="properties",
            field=models.ManyToManyField(
                related_name="templates", to="voucher_app.templateproperty"
            ),
        ),
        migrations.AlterField(
            model_name="templateproperty",
            name="property_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="voucher_app.templatepropertytype",
            ),
        ),
    ]