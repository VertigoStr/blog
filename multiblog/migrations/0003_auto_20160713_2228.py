# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('multiblog', '0002_auto_20160713_1952'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogger',
            options={'verbose_name': 'Блоггер', 'verbose_name_plural': 'Блоггеры'},
        ),
    ]
