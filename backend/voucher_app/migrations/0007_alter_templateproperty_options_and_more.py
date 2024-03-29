# Generated by Django 4.1.5 on 2023-06-01 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("voucher_app", "0006_alter_templateproperty_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="templateproperty",
            options={
                "ordering": ["pk"],
                "verbose_name": "TemplateProperty",
                "verbose_name_plural": "TemplateProperties",
            },
        ),
        migrations.AlterModelOptions(
            name="templatepropertytype",
            options={
                "verbose_name": "Template property type",
                "verbose_name_plural": "Template proeprty types",
            },
        ),
        migrations.AlterField(
            model_name="template",
            name="properties",
            field=models.ManyToManyField(
                related_name="templates",
                to="voucher_app.templateproperty",
                verbose_name="AAAAAAAAAAAAA",
            ),
        ),
    ]
