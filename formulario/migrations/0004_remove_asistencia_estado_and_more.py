# Generated by Django 5.1.6 on 2025-03-20 16:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formulario', '0003_asistencia_estado_participante_fecha_inscripcion_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='asistencia',
            name='estado',
        ),
        migrations.AlterField(
            model_name='asistencia',
            name='fecha_asistencia',
            field=models.DateField(blank=True, default=datetime.date.today, null=True),
        ),
        migrations.AlterField(
            model_name='participante',
            name='fecha_inscripcion',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.DeleteModel(
            name='Pago',
        ),
    ]
