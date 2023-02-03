# Generated by Django 4.1.5 on 2023-01-22 15:37

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voucher_app', '0002_alter_template_title_requestorder'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestorder',
            name='addresses',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.EmailField(max_length=254), default=list, size=None),
        ),
    ]
