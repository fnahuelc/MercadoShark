# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-25 07:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managerApp', '0004_auto_20170325_0714'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='image',
            field=models.URLField(verbose_name='https://http2.mlstatic.com/notebook-asus-f555ua-eh71-core-i7-6gen-1tb-8gb-156-pulgadas-D_NQ_NP_971115-MLA25208512372_122016-O.webp'),
        ),
    ]
