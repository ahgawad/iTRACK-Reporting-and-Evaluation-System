# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2019-01-26 03:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('perform', '0008_performanceindicatortaskbenchmark_performanceindicatortasktarget'),
    ]

    operations = [
        migrations.RenameField(
            model_name='performanceindicatortaskbenchmark',
            old_name='pitid',
            new_name='pibid',
        ),
    ]