# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2019-01-26 03:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perform', '0009_auto_20190126_0400'),
    ]

    operations = [
        migrations.AlterField(
            model_name='performanceindicatortaskbenchmark',
            name='indicator_task_benchmark',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
        migrations.AlterField(
            model_name='performanceindicatortasktarget',
            name='indicator_task_target',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
    ]
