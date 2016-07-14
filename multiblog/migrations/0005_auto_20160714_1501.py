# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('multiblog', '0004_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogger',
            name='avatar',
            field=models.ImageField(default='./media/img/ava-default.png', verbose_name='Аватар', upload_to='./media/img/'),
        ),
    ]
