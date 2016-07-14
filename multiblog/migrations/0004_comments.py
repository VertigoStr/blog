# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('multiblog', '0003_auto_20160713_2228'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('text', models.TextField(verbose_name='Текст')),
                ('time', models.DateTimeField(verbose_name='Дата публикации')),
                ('author', models.ForeignKey(verbose_name='Автор', to=settings.AUTH_USER_MODEL)),
                ('publication', models.ForeignKey(verbose_name='Публикация', to='multiblog.Publication')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
            },
        ),
    ]
