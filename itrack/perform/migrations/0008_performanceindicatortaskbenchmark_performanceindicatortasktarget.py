# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2019-01-26 03:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20190120_0117'),
        ('perform', '0007_auto_20190120_1833'),
    ]

    operations = [
        migrations.CreateModel(
            name='PerformanceIndicatorTaskBenchmark',
            fields=[
                ('pitid', models.AutoField(primary_key=True, serialize=False, verbose_name='Log Indicator Benchmark ID')),
                ('indicator_task_benchmark', models.IntegerField(default=0)),
                ('piid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='perform.PerformanceIndicator')),
                ('taid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Task')),
            ],
        ),
        migrations.CreateModel(
            name='PerformanceIndicatorTaskTarget',
            fields=[
                ('pitid', models.AutoField(primary_key=True, serialize=False, verbose_name='Log Indicator Target ID')),
                ('indicator_task_target', models.IntegerField(default=0)),
                ('piid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='perform.PerformanceIndicator')),
                ('taid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Task')),
            ],
        ),
    ]