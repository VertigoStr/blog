# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-19 11:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('multiblog', '0009_publication_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='multiblog.Categories', verbose_name='Категория'),
        ),
    ]
