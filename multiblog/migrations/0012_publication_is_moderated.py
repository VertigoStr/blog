# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-19 15:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('multiblog', '0011_auto_20160719_1655'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='is_moderated',
            field=models.BooleanField(default=False, verbose_name='На модерации'),
        ),
    ]
