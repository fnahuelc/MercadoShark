# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-25 01:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managerApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='image',
            field=models.FileField(default='', upload_to=b''),
            preserve_default=False,
        ),
    ]
