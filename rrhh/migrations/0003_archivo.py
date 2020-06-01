# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2020-06-01 13:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rrhh', '0002_entrevista'),
    ]

    operations = [
        migrations.CreateModel(
            name='Archivo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=255)),
                ('archivo', models.FileField(upload_to='')),
                ('funcionario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rrhh.Funcionario')),
            ],
        ),
    ]
