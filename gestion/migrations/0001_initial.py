# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2020-04-02 22:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Colegio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('modificado_en', models.DateTimeField(auto_now=True)),
                ('nombre', models.CharField(max_length=250)),
                ('abrev', models.CharField(max_length=50, verbose_name='Abreviación')),
                ('rbd', models.CharField(blank=True, max_length=50, null=True, verbose_name='Rol de base de datos (RBD)')),
                ('estado', models.CharField(choices=[('gratuito', 'Gratuito'), ('particular_subvencionado', 'Particular Subvencionado'), ('particular', 'Particular')], default='particular_subvencionado', max_length=25)),
                ('tipo_jornada', models.CharField(choices=[('media', 'Media Jornada'), ('completa', 'Jornada Completa')], default='completa', max_length=25)),
                ('total_salas', models.PositiveIntegerField(blank=True, null=True, verbose_name='Total de salas')),
                ('capacidad_promedio_salas', models.PositiveIntegerField(blank=True, null=True, verbose_name='Capacidad promedio de las salas')),
                ('total_matricula_ultimo_anio', models.PositiveIntegerField(blank=True, null=True, verbose_name='Total de matricula el último año')),
                ('total_profesores_aula', models.PositiveIntegerField(blank=True, null=True, verbose_name='Total de profesores de aula')),
                ('total_profesionales_educacion', models.PositiveIntegerField(blank=True, null=True, verbose_name='Total de profesionales de la educación')),
                ('total_asistentes_educacion', models.PositiveIntegerField(blank=True, null=True, verbose_name='Total de asistentes de la educación')),
                ('total_alumnos_pie', models.PositiveIntegerField(blank=True, null=True, verbose_name='Total de alumnos en PIE')),
                ('indice_vulnerabilidad', models.CharField(blank=True, max_length=25, null=True, verbose_name='Índice de vulnerabilidad')),
            ],
            options={
                'verbose_name': 'Colegio',
                'verbose_name_plural': 'Colegios',
            },
        ),
        migrations.CreateModel(
            name='ExcelenciaAcademica',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('modificado_en', models.DateTimeField(auto_now=True)),
                ('detalle', models.TextField(max_length=2500)),
                ('anio', models.PositiveIntegerField(verbose_name='Año')),
            ],
            options={
                'verbose_name': 'Excelencia Académica',
                'verbose_name_plural': 'Excelencias Académicas',
            },
        ),
        migrations.CreateModel(
            name='Fundacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('modificado_en', models.DateTimeField(auto_now=True)),
                ('nombre', models.CharField(max_length=250)),
            ],
            options={
                'verbose_name': 'Fundación',
                'verbose_name_plural': 'Fundaciones',
            },
        ),
        migrations.CreateModel(
            name='Periodo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('modificado_en', models.DateTimeField(auto_now=True)),
                ('nombre', models.CharField(max_length=250)),
                ('anio', models.PositiveIntegerField(verbose_name='Año')),
                ('activo', models.BooleanField(default=False)),
                ('colegio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion.Colegio')),
            ],
            options={
                'verbose_name': 'Periodo',
                'verbose_name_plural': 'Periodos',
            },
        ),
        migrations.CreateModel(
            name='Union',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('modificado_en', models.DateTimeField(auto_now=True)),
                ('nombre', models.CharField(max_length=250)),
            ],
            options={
                'verbose_name': 'Union',
                'verbose_name_plural': 'Uniones',
            },
        ),
    ]