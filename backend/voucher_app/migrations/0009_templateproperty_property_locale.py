# Generated by Django 4.1.5 on 2023-06-04 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("voucher_app", "0008_remove_template_properties_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="templateproperty",
            name="property_locale",
            field=models.CharField(
                default="text", max_length=60, verbose_name="Template part"
            ),
            preserve_default=False,
        ),
    ]
