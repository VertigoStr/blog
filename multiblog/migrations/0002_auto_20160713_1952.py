# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('multiblog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Имя')),
                ('abstract', models.TextField(max_length=600, verbose_name='Краткое содержание')),
                ('full_text', models.TextField(verbose_name='Полное описание')),
                ('time', models.DateTimeField(verbose_name='Дата публикации')),
            ],
            options={
                'verbose_name_plural': 'Публикации',
                'verbose_name': 'Публикация',
            },
        ),
        migrations.AlterModelOptions(
            name='blogger',
            options={},
        ),
        migrations.AddField(
            model_name='publication',
            name='author',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
    ]
