# Generated by Django 4.1.5 on 2023-06-01 10:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("voucher_app", "0005_alter_templatepropertytype_name"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="templateproperty",
            options={
                "ordering": ["pk"],
                "verbose_name": "TemplateProperty111",
                "verbose_name_plural": "TemplateProperties222",
            },
        ),
    ]
