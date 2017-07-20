# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-15 14:48
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('created', models.DateTimeField(auto_created=True)),
                ('id', models.IntegerField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=250, validators=[django.core.validators.EmailValidator()])),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]