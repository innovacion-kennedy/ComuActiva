# Generated by Django 5.1.6 on 2025-03-21 04:38

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formulario', '0005_participante_area_participante_barrio_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Acudiente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre del Acudiente')),
                ('telefono', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(message='El teléfono debe contener solo números.', regex='^\\d{7,15}$')], verbose_name='Teléfono')),
                ('ocupacion', models.CharField(max_length=100, verbose_name='Ocupación')),
                ('parentesco', models.CharField(choices=[('Padre', 'Padre'), ('Madre', 'Madre'), ('Tío', 'Tío'), ('Tía', 'Tía'), ('Hermano', 'Hermano'), ('Hermana', 'Hermana'), ('Otro', 'Otro')], max_length=50, verbose_name='Parentesco')),
                ('direccion', models.TextField(verbose_name='Dirección')),
            ],
            options={
                'db_table': 'formulario_acudiente',
            },
        ),
        migrations.CreateModel(
            name='NivelEducativo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(choices=[('Básica Primaria', 'Básica Primaria'), ('Básica Secundaria', 'Básica Secundaria'), ('Técnico', 'Técnico'), ('Tecnólogo', 'Tecnólogo'), ('Universitaria Incompleta', 'Universitaria Incompleta'), ('Universitaria Completa', 'Universitaria Completa'), ('Posgrado Incompleto', 'Posgrado Incompleto'), ('Posgrado Completo', 'Posgrado Completo'), ('Maestría', 'Maestría'), ('Ninguno', 'Ninguno'), ('Otro', 'Otro')], max_length=50, unique=True)),
            ],
            options={
                'db_table': 'formulario_nivel_educativo',
            },
        ),
        migrations.AlterField(
            model_name='participante',
            name='barrio',
            field=models.CharField(blank=True, choices=[('agrupacion pio x', 'agrupacion pio x'), ('agrupacion multifamiliar villa emilia', 'agrupacion multifamiliar villa emilia'), ('alferez real', 'alferez real'), ('americas central', 'americas central'), ('americas occidental i. ii y iii etapa', 'americas occidental i. ii y iii etapa'), ('antiguo hipodromo de techo ii etapa', 'antiguo hipodromo de techo ii etapa'), ('carvajal ii sector', 'carvajal ii sector'), ('centroamericas', 'centroamericas'), ('ciudad kennedy', 'ciudad kennedy'), ('conjunto res. el rincon de mandalay', 'conjunto res. el rincon de mandalay'), ('floresta sur', 'floresta sur'), ('fundadores', 'fundadores'), ('glorieta de las americas', 'glorieta de las americas'), ('hipotecho', 'hipotecho'), ('igualdad i sector', 'igualdad i sector'), ('igualdad ii sector', 'igualdad ii sector'), ('la floresta', 'la floresta'), ('la igualdad', 'la igualdad'), ('la llanura', 'la llanura'), ('la llanura manzana p', 'la llanura manzana p'), ('las americas', 'las americas'), ('las americas sector galan', 'las americas sector galan'), ('los sauces', 'los sauces'), ('mandalay etapa a sector ii', 'mandalay etapa a sector ii'), ('mandalay i sector', 'mandalay i sector'), ('marsella iii sector', 'marsella iii sector'), ('multifamiliares villa adriana mz. h', 'multifamiliares villa adriana mz. h'), ('nueva marsella i. ii y iii sector', 'nueva marsella i. ii y iii sector'), ('provivienda oriental', 'provivienda oriental'), ('santa rosa de carvajal', 'santa rosa de carvajal'), ('urb. los laureles (sauces-robles)', 'urb. los laureles (sauces-robles)'), ('villa adriana', 'villa adriana'), ('villa claudia', 'villa claudia'), ('urbanizacion castilla la nueva', 'urbanizacion castilla la nueva')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='participante',
            name='pais_origen',
            field=models.CharField(choices=[('Afganistán', 'Afganistán'), ('Albania', 'Albania'), ('Alemania', 'Alemania'), ('Andorra', 'Andorra'), ('Angola', 'Angola'), ('Antigua y Barbuda', 'Antigua y Barbuda'), ('Arabia Saudita', 'Arabia Saudita'), ('Argelia', 'Argelia'), ('Argentina', 'Argentina'), ('Armenia', 'Armenia'), ('Australia', 'Australia'), ('Austria', 'Austria'), ('Brasil', 'Brasil'), ('Canadá', 'Canadá'), ('Colombia', 'Colombia'), ('Estados Unidos', 'Estados Unidos'), ('Francia', 'Francia'), ('Micronesia', 'Micronesia'), ('Moldavia', 'Moldavia'), ('Mónaco', 'Mónaco'), ('Mongolia', 'Mongolia'), ('Montenegro', 'Montenegro'), ('Mozambique', 'Mozambique'), ('Namibia', 'Namibia'), ('Nauru', 'Nauru'), ('Nepal', 'Nepal'), ('Nicaragua', 'Nicaragua'), ('Níger', 'Níger'), ('Nigeria', 'Nigeria'), ('Noruega', 'Noruega'), ('Nueva Zelanda', 'Nueva Zelanda'), ('Omán', 'Omán'), ('Pakistán', 'Pakistán'), ('Palaos', 'Palaos'), ('Panamá', 'Panamá'), ('Papúa Nueva Guinea', 'Papúa Nueva Guinea'), ('Paraguay', 'Paraguay'), ('Países Bajos', 'Países Bajos'), ('Perú', 'Perú'), ('Polonia', 'Polonia'), ('Portugal', 'Portugal'), ('Reino Unido', 'Reino Unido'), ('República Centroafricana', 'República Centroafricana'), ('República Checa', 'República Checa'), ('República Democrática del Congo', 'República Democrática del Congo'), ('República Dominicana', 'República Dominicana'), ('República del Congo', 'República del Congo'), ('Ruanda', 'Ruanda'), ('Rumanía', 'Rumanía'), ('Rusia', 'Rusia'), ('Samoa', 'Samoa'), ('San Cristóbal y Nieves', 'San Cristóbal y Nieves'), ('San Marino', 'San Marino'), ('San Vicente y las Granadinas', 'San Vicente y las Granadinas'), ('Santa Lucía', 'Santa Lucía'), ('Santo Tomé y Príncipe', 'Santo Tomé y Príncipe'), ('Senegal', 'Senegal'), ('Serbia', 'Serbia'), ('Seychelles', 'Seychelles'), ('Sierra Leona', 'Sierra Leona'), ('Singapur', 'Singapur'), ('Siria', 'Siria'), ('Somalia', 'Somalia'), ('Sri Lanka', 'Sri Lanka'), ('Suazilandia', 'Suazilandia'), ('Sudáfrica', 'Sudáfrica'), ('Sudán', 'Sudán'), ('Sudán del Sur', 'Sudán del Sur'), ('Suecia', 'Suecia'), ('Suiza', 'Suiza'), ('Surinam', 'Surinam'), ('Tailandia', 'Tailandia'), ('Tanzania', 'Tanzania'), ('Tayikistán', 'Tayikistán'), ('Timor Oriental', 'Timor Oriental'), ('Togo', 'Togo'), ('Tonga', 'Tonga'), ('Trinidad y Tobago', 'Trinidad y Tobago'), ('Túnez', 'Túnez'), ('Turkmenistán', 'Turkmenistán'), ('Turquía', 'Turquía'), ('Tuvalu', 'Tuvalu'), ('Ucrania', 'Ucrania'), ('Uganda', 'Uganda'), ('Uruguay', 'Uruguay'), ('Uzbekistán', 'Uzbekistán'), ('Vanuatu', 'Vanuatu'), ('Venezuela', 'Venezuela'), ('Vietnam', 'Vietnam'), ('Yemen', 'Yemen'), ('Yibuti', 'Yibuti'), ('Zambia', 'Zambia'), ('Zimbabue', 'Zimbabue')], default='Colombia', max_length=50),
        ),
        migrations.CreateModel(
            name='DatosComplementarios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identidad_genero', models.CharField(choices=[('Masculino', 'Masculino'), ('Femenino', 'Femenino'), ('Transgénero', 'Transgénero'), ('Intersexual', 'Intersexual'), ('Otro', 'Otro'), ('No Responde', 'No Responde')], max_length=20)),
                ('grupo_etnico', models.CharField(choices=[('Indígena', 'Indígena'), ('Afro', 'Afro'), ('Comunidad Negra', 'Comunidad Negra'), ('Palenquero', 'Palenquero'), ('Raizal', 'Raizal'), ('Rom o Gitano', 'Rom o Gitano'), ('Ninguno', 'Ninguno')], max_length=20)),
                ('discapacidad', models.CharField(choices=[('No', 'No'), ('Auditiva', 'Auditiva'), ('Física', 'Física'), ('Intelectual', 'Intelectual'), ('Visual', 'Visual'), ('Sordo-Ceguera', 'Sordo-Ceguera'), ('Psicosocial', 'Psicosocial'), ('Múltiple', 'Múltiple')], default='No', max_length=20)),
                ('tipo_discapacidad', models.CharField(blank=True, choices=[('Auditiva', 'Auditiva'), ('Física', 'Física'), ('Intelectual', 'Intelectual'), ('Visual', 'Visual'), ('Sordo-Ceguera', 'Sordo-Ceguera'), ('Psicosocial', 'Psicosocial'), ('Múltiple', 'Múltiple')], max_length=50, null=True)),
                ('enfermedad_huerfana', models.BooleanField(default=False)),
                ('enfermedad_nombre', models.CharField(blank=True, max_length=100, null=True)),
                ('conflicto_armado', models.BooleanField(default=False)),
                ('tipo_sangre', models.CharField(choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B-'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')], max_length=5)),
                ('otro_nivel_educativo', models.CharField(blank=True, max_length=100, null=True)),
                ('pertenece_organizacion', models.BooleanField(default=False)),
                ('nombre_organizacion', models.CharField(blank=True, max_length=100, null=True)),
                ('participante', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='datos_complementarios', to='formulario.participante')),
                ('nivel_educativo', models.ManyToManyField(blank=True, to='formulario.niveleducativo')),
            ],
            options={
                'db_table': 'formulario_datos_complementarios',
            },
        ),
    ]
