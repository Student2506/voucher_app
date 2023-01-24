# Generated by Django 4.1.5 on 2023-01-20 10:48

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies: migrations.migration.Migration.dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Template',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('template_content', models.TextField(blank=True, verbose_name='template_content')),
            ],
            options={
                'verbose_name': 'Template',
                'verbose_name_plural': 'Templates',
                'db_table': 'voucher_app"."template',
                'ordering': ['title'],
            },
        ),
    ]