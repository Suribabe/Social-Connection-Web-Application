# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-16 00:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0012_auto_20161015_0412'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='last_modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
