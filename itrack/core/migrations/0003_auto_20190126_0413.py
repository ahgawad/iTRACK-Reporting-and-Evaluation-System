# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2019-01-26 03:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20190120_0117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setting',
            name='setting_value',
            field=models.FloatField(default=0),
        ),
    ]
