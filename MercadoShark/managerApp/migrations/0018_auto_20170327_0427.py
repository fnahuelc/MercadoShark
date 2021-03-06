# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-27 04:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managerApp', '0017_auto_20170327_0305'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='quantity',
            new_name='available_quantity',
        ),
        migrations.RemoveField(
            model_name='article',
            name='image',
        ),
        migrations.AddField(
            model_name='article',
            name='buying_mode',
            field=models.CharField(default=0, max_length=60),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='article',
            name='category_id',
            field=models.CharField(default=1, max_length=60),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='article',
            name='condition',
            field=models.CharField(default=1, max_length=60),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='article',
            name='currency_id',
            field=models.CharField(default=1, max_length=60),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='article',
            name='listing_type_id',
            field=models.CharField(default=1, max_length=60),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='article',
            name='pictures',
            field=models.CharField(default=1, max_length=2000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='article',
            name='video_id',
            field=models.CharField(default=1, max_length=60),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='article',
            name='warranty',
            field=models.CharField(default=1, max_length=60),
            preserve_default=False,
        ),
    ]
