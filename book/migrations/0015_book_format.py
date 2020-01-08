# Generated by Django 2.2.4 on 2019-09-17 09:19

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0014_book_cover'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='format',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={}),
            preserve_default=False,
        ),
    ]