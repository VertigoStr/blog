# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-19 13:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('multiblog', '0010_auto_20160719_1431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogger',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
