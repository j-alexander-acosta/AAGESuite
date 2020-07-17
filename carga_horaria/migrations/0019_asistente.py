# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2020-06-30 19:46
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('carga_horaria', '0018_auto_20200617_0458'),
    ]

    operations = [
        migrations.CreateModel(
            name='Asistente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('horas', models.DecimalField(decimal_places=1, max_digits=3, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(44)])),
                ('funcion', models.CharField(max_length=255)),
                ('fundacion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='carga_horaria.Fundacion')),
            ],
        ),
    ]