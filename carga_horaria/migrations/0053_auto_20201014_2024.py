# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-10-14 20:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('carga_horaria', '0052_remove_profesor_horas_no_aula'),
    ]

    operations = [
        migrations.AddField(
            model_name='colegio',
            name='periodo',
            field=models.PositiveSmallIntegerField(default=2020),
        ),
        migrations.AlterField(
            model_name='periodo',
            name='colegio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='carga_horaria.Colegio'),
        ),
    ]