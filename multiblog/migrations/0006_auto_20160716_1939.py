# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('multiblog', '0005_auto_20160714_1501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogger',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Имя', blank=True),
        ),
        migrations.AlterField(
            model_name='blogger',
            name='phone',
            field=models.CharField(max_length=20, verbose_name='Телефон', blank=True),
        ),
        migrations.AlterField(
            model_name='blogger',
            name='skype',
            field=models.CharField(max_length=20, verbose_name='Skype', blank=True),
        ),
        migrations.AlterField(
            model_name='blogger',
            name='surname',
            field=models.CharField(max_length=100, verbose_name='Фамилия', blank=True),
        ),
    ]
