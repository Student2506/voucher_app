# Generated by Django 4.1.5 on 2023-01-30 14:05

import tinymce.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('voucher_app', '0010_remove_requestorder_code_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='template',
            name='template_content',
            field=tinymce.models.HTMLField(blank=True, verbose_name='template_content'),
        ),
    ]
