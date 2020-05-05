# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2020-04-09 13:38
from __future__ import unicode_literals

import carga_horaria.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Asignacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('horas', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Asignatura',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('horas', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='AsignaturaBase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('horas_jec', models.PositiveSmallIntegerField()),
                ('horas_nec', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Colegio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('jec', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('letra', models.CharField(max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Periodo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('colegio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carga_horaria.Colegio')),
            ],
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('nivel', models.CharField(choices=[(carga_horaria.models.Nivel('Pre kinder'), 'Pre kinder'), (carga_horaria.models.Nivel('Kinder'), 'Kinder'), (carga_horaria.models.Nivel('Primero básico'), 'Primero básico'), (carga_horaria.models.Nivel('Segundo básico'), 'Segundo básico'), (carga_horaria.models.Nivel('Tercero básico'), 'Tercero básico'), (carga_horaria.models.Nivel('Cuarto básico'), 'Cuarto básico'), (carga_horaria.models.Nivel('Quinto básico'), 'Quinto básico'), (carga_horaria.models.Nivel('Sexto básico'), 'Sexto básico'), (carga_horaria.models.Nivel('Séptimo básico'), 'Séptimo básico'), (carga_horaria.models.Nivel('Octavo básico'), 'Octavo básico'), (carga_horaria.models.Nivel('Primero medio'), 'Primero medio'), (carga_horaria.models.Nivel('Segundo medio'), 'Segundo medio'), (carga_horaria.models.Nivel('Tercero medio'), 'Tercero medio'), (carga_horaria.models.Nivel('Cuarto medio'), 'Cuarto medio')], max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='Profesor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('horas', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='periodo',
            name='plan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carga_horaria.Plan'),
        ),
        migrations.AddField(
            model_name='curso',
            name='periodo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carga_horaria.Periodo'),
        ),
        migrations.AddField(
            model_name='asignaturabase',
            name='plan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carga_horaria.Plan'),
        ),
        migrations.AddField(
            model_name='asignatura',
            name='base',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carga_horaria.AsignaturaBase'),
        ),
        migrations.AddField(
            model_name='asignatura',
            name='periodo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carga_horaria.Periodo'),
        ),
        migrations.AddField(
            model_name='asignacion',
            name='asignatura',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carga_horaria.Asignatura'),
        ),
        migrations.AddField(
            model_name='asignacion',
            name='profesor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carga_horaria.Profesor'),
        ),
    ]