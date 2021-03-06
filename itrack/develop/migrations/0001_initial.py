# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2019-01-19 18:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ITRACKComponentDevelopmentIndicator',
            fields=[
                ('iciid', models.AutoField(primary_key=True, serialize=False, verbose_name='iTRACK Component Development Indicator ID')),
                ('indicator_name', models.CharField(max_length=200)),
                ('is_percentage', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ITRACKComponentElement',
            fields=[
                ('iceid', models.AutoField(primary_key=True, serialize=False, verbose_name='iTRACK Component Element ID')),
                ('itrack_component_element_name', models.CharField(max_length=200)),
                ('icid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.ITRACKComponent')),
            ],
        ),
        migrations.CreateModel(
            name='ITRACKComponentElementIndicatorValue',
            fields=[
                ('iceivid', models.AutoField(primary_key=True, serialize=False, verbose_name='iTRACK Component Element Development Indicator Value ID')),
                ('indicator_value', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('iceid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='develop.ITRACKComponentElement')),
                ('iciid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='develop.ITRACKComponentDevelopmentIndicator')),
                ('icvid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.ITRACKComponentVersion')),
            ],
        ),
        migrations.CreateModel(
            name='ITRACKComponentIndicatorValue',
            fields=[
                ('icivid', models.AutoField(primary_key=True, serialize=False, verbose_name='iTRACK Component Development Indicator Value ID')),
                ('indicator_value', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('icid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.ITRACKComponent')),
                ('iciid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='develop.ITRACKComponentDevelopmentIndicator')),
                ('icvid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.ITRACKComponentVersion')),
            ],
        ),
    ]
