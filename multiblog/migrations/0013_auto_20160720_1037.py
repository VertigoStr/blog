# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-20 07:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('multiblog', '0012_publication_is_moderated'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='is_canceled',
            field=models.BooleanField(default=False, verbose_name='Отклонено?'),
        ),
        migrations.AddField(
            model_name='publication',
            name='is_new',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='publication',
            name='why_not',
            field=models.TextField(default='', max_length=600, verbose_name='Причина отказа'),
        ),
        migrations.AlterField(
            model_name='publication',
            name='is_moderated',
            field=models.BooleanField(default=False, verbose_name='На модерации?'),
        ),
    ]
