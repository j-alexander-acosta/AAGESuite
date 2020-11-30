# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2020-11-29 23:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rrhh', '0029_auto_20201129_2256'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contratocolegio',
            name='reemplazando',
        ),
        migrations.AddField(
            model_name='contratocolegio',
            name='reemplazando_licencia',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='rrhh.LicenciaFuncionarioColegio', verbose_name='En reemplazo de'),
        ),
        migrations.AlterField(
            model_name='documentofuncionario',
            name='tipo_documento',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='rrhh.TipoDocumento'),
        ),
    ]
