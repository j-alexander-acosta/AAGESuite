# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2020-05-29 13:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Funcionario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('rut', models.CharField(max_length=16)),
                ('fecha_nacimiento', models.DateField(verbose_name='Fecha de nacimiento')),
                ('fecha_ingreso', models.DateField(verbose_name='Fecha ingreso SEA')),
                ('titulo', models.CharField(max_length=255)),
                ('religion', models.CharField(max_length=255)),
                ('estado_civil', models.CharField(max_length=255)),
                ('nacionalidad', models.CharField(max_length=255)),
                ('sexo', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('direccion', models.CharField(max_length=255)),
                ('telefono', models.CharField(max_length=15)),
            ],
            options={
                'verbose_name': 'Funcionario',
                'verbose_name_plural': 'Funcionarios',
            },
        ),
    ]
