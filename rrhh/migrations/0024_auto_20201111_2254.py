# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2020-11-11 22:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rrhh', '0023_auto_20201109_2043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentofuncionario',
            name='tipo_documento',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='rrhh.TipoDocumento'),
        ),
        migrations.AlterField(
            model_name='estadosolicitud',
            name='estado',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Aceptada'), (2, 'Pendiente'), (3, 'Rechazada'), (4, 'En espera de candidatos'), (5, 'Aprobada')], default=2),
        ),
        migrations.AlterField(
            model_name='estadosolicitud',
            name='observaciones',
            field=models.TextField(blank=True, max_length=2500, null=True),
        ),
        migrations.AlterField(
            model_name='estadosolicitud',
            name='voto',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Voto de autorización'),
        ),
        migrations.AlterField(
            model_name='solicitudcontratacion',
            name='postulantes',
            field=models.ManyToManyField(blank=True, to='rrhh.Persona'),
        ),
    ]
