# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2019-01-26 03:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perform', '0010_auto_20190126_0404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='performanceindicatorvalue',
            name='indicator_value',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
    ]
