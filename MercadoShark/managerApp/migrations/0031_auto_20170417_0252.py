# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-04-17 02:52
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('managerApp', '0030_auto_20170417_0202'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userId', models.CharField(max_length=100)),
                ('test_account', models.BooleanField(default=False)),
                ('access_token', models.CharField(default='No acces token', max_length=200)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='mluser',
            name='user',
        ),
        migrations.RemoveField(
            model_name='item',
            name='account',
        ),
        migrations.DeleteModel(
            name='MlUser',
        ),
    ]