# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2020-05-18 02:37
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carga_horaria', '0014_periodo_horas'),
    ]

    operations = [
        migrations.AddField(
            model_name='periodo',
            name='horas_dif',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=3, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(9)]),
        ),
    ]
