# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-11 17:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0005_auto_20161011_1745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='profile',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='grumblr.Profile'),
        ),
    ]
