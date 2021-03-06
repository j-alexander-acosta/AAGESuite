# Generated by Django 2.2 on 2021-10-18 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evado', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='periodoencuesta',
            name='anio',
            field=models.PositiveIntegerField(blank=True, max_length=4, null=True, verbose_name='Año'),
        ),
        migrations.AddField(
            model_name='periodoencuesta',
            name='periodo',
            field=models.CharField(blank=True, choices=[('verano', 'Verano'), ('primer_semestre', 'Primer Semestre'), ('invierno', 'Invierno'), ('segundo_semestre', 'Segundo Semestre')], max_length=25, null=True),
        ),
    ]
