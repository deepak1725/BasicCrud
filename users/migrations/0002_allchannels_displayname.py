# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-01-07 16:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='allchannels',
            name='displayName',
            field=models.CharField(default='NoNam', max_length=50),
            preserve_default=False,
        ),
    ]
