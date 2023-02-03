# Generated by Django 4.1.5 on 2023-01-20 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies: list[tuple[str, str]] = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('sname', models.CharField(db_column='sName', max_length=50, verbose_name='Наименование организации')),
                ('iid', models.IntegerField(db_column='lID', primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'tblClient',
                'managed': False,
            },
        ),
    ]
