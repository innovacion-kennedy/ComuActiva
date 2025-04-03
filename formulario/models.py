from django.db import models
from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import date
from django.core.validators import RegexValidator
from .choices import (
    TIPO_AREA_CHOICES, DISCIPLINAS_DEPORTE, DISCIPLINAS_CULTURA,
    PAIS_CHOICES, BARRIO_CHOICES, DISCAPACIDAD_BOOLEAN_CHOICES,
    EDUCACION_CHOICES, GENERO_CHOICES, ETNIA_CHOICES, SANGRE_CHOICES,
    TIPOS_DISCAPACIDAD
)

class Curso(models.Model):
    CURSOS_OPCIONES = [
        ("Fútbol", "Fútbol"),
        ("Basketball", "Basketball"),
        ("Voleibol", "Voleibol"),
        ("Danza", "Danza"),
        ("Fotografía", "Fotografía"),
    ]
    nombre = models.CharField(max_length=50, choices=CURSOS_OPCIONES, unique=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'formulario_curso'

class Docente(models.Model):
    nombre = models.CharField(max_length=100)
    identificacion = models.CharField(max_length=30, unique=True)
    correo = models.EmailField(unique=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=30, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    area_encargada = models.CharField(max_length=50, choices=TIPO_AREA_CHOICES, blank=True, null=True)
    disciplina = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} - {self.identificacion}"

    class Meta:
        db_table = 'formulario_docente'

class Participante(models.Model):
    TIPO_DOCUMENTO_CHOICES = [
        ('CC', 'Cédula de Ciudadanía'),
        ('TI', 'Tarjeta de Identidad'),
        ('CE', 'Cédula de Extranjería'),
    ]

    AREA_CHOICES = [
        ('Rural', 'Rural'),
        ('Urbano', 'Urbano'),
    ]

    nombre = models.CharField(max_length=100)
    tipo_documento = models.CharField(max_length=2, choices=TIPO_DOCUMENTO_CHOICES, default='CC')
    identificacion = models.CharField(max_length=30, unique=True)
    fecha_expedicion = models.DateField(blank=True, null=True)
    correo = models.EmailField(unique=True)
    direccion = models.TextField(blank=True, null=True)
    telefono = models.CharField(max_length=30, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    curso_extendido = models.ForeignKey('CursoExtendido', on_delete=models.SET_NULL, blank=True, null=True, related_name='participantes')
    curso = models.ForeignKey(Curso, on_delete=models.SET_NULL, blank=True, null=True)
    edad = models.IntegerField(blank=True, null=True)
    fecha_inscripcion = models.DateField(auto_now_add=True)
    lugar_expedicion = models.CharField(max_length=100, blank=True, null=True)
    pais_origen = models.CharField(max_length=50, choices=PAIS_CHOICES, default='Colombia')
    ciudad = models.CharField(max_length=100, default="Bogotá")
    area = models.CharField(max_length=10, choices=AREA_CHOICES, default="Urbano")
    localidad = models.CharField(max_length=100, default="Kennedy")
    barrio = models.CharField(max_length=100, choices=BARRIO_CHOICES, blank=True, null=True)

    def calcular_edad(self):
        if self.fecha_nacimiento:
            today = date.today()
            return today.year - self.fecha_nacimiento.year - ((today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))
        return None

    def save(self, *args, **kwargs):
        self.edad = self.calcular_edad()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} - {self.identificacion}"

    class Meta:
        db_table = 'formulario_participante'

class Clase(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE)
    fecha_clase = models.DateField(default=date.today)
    cupo_maximo = models.IntegerField(default=30)
    cupo_actual = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.curso} - {self.docente}"

    class Meta:
        db_table = 'formulario_clase'

class Asistencia(models.Model):
    alumno = models.ForeignKey(Participante, on_delete=models.CASCADE, blank=True, null=True)
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE)
    fecha_asistencia = models.DateField(blank=True, null=True, default=date.today)

    def __str__(self):
        return f"Asistencia: {self.alumno} - {self.clase}"

    class Meta:
        db_table = 'formulario_asistencia'

class ActividadCultura(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'formulario_actividad_cultura'

class Proyecto(models.Model):
    nombre = models.CharField(max_length=100, default="Proyecto sin nombre")
    descripcion = models.TextField(blank=True, null=True, default="Sin descripción")
    fecha_inicio = models.DateField(default=date.today)
    fecha_fin = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'formulario_proyecto'

class DatosComplementarios(models.Model):
    participante = models.OneToOneField('Participante', on_delete=models.CASCADE, related_name='datos_complementarios')
    identidad_genero = models.CharField(max_length=20, choices=GENERO_CHOICES)
    grupo_etnico = models.CharField(max_length=20, choices=ETNIA_CHOICES)
    discapacidad = models.CharField(max_length=20, choices=DISCAPACIDAD_BOOLEAN_CHOICES, default="No")
    tipo_discapacidad = models.CharField(max_length=50, choices=TIPOS_DISCAPACIDAD, blank=True, null=True)
    enfermedad_huerfana = models.BooleanField(default=False)
    enfermedad_nombre = models.CharField(max_length=100, blank=True, null=True)
    conflicto_armado = models.BooleanField(default=False)
    tipo_sangre = models.CharField(max_length=5, choices=SANGRE_CHOICES)
    nivel_educativo = models.ManyToManyField('NivelEducativo', blank=True)
    otro_nivel_educativo = models.CharField(max_length=100, blank=True, null=True)
    pertenece_organizacion = models.BooleanField(default=False)
    nombre_organizacion = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Datos complementarios de {self.participante.nombre}"

    class Meta:
        db_table = 'formulario_datos_complementarios'

class NivelEducativo(models.Model):
    nombre = models.CharField(max_length=50, choices=EDUCACION_CHOICES, unique=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'formulario_nivel_educativo'

class Acudiente(models.Model):
    participante = models.ForeignKey(Participante, on_delete=models.CASCADE, related_name='acudientes', null=True, blank=True)
    nombre = models.CharField(max_length=50, verbose_name="Nombre del Acudiente")
    telefono = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\d{7,15}$', message="El teléfono debe contener solo números (7 a 15 dígitos).")],
        verbose_name="Teléfono"
    )
    ocupacion = models.CharField(max_length=100, verbose_name="Ocupación")
    parentesco = models.CharField(
        max_length=50,
        choices=[('Padre', 'Padre'), ('Madre', 'Madre'), ('Tío', 'Tío'),
                 ('Tía', 'Tía'), ('Hermano', 'Hermano'), ('Hermana', 'Hermana'), ('Otro', 'Otro')],
        verbose_name="Parentesco"
    )
    direccion = models.TextField(verbose_name="Dirección")

    def __str__(self):
        return f"{self.nombre} ({self.parentesco})"

    class Meta:
        db_table = "formulario_acudiente"
        
        
class Disciplina(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    tipo = models.CharField(max_length=50, choices=TIPO_AREA_CHOICES)

    def __str__(self):
        return f"{self.nombre} ({self.tipo})"



class CursoExtendido(models.Model):
    tipo_curso = models.CharField(max_length=20, choices=TIPO_AREA_CHOICES)
    disciplina = models.ForeignKey('Disciplina', on_delete=models.CASCADE)
    horario = models.CharField(max_length=100)
    lugar = models.CharField(max_length=150)
    docente = models.ForeignKey('Docente', on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        return f"{self.tipo_curso} - {self.disciplina} ({self.horario})"

class DocumentoRequisito(models.Model):
    participante = models.ForeignKey(Participante, on_delete=models.CASCADE)
    formulario_inscripcion_firmado = models.FileField(upload_to='documentos/')
    documento_identidad = models.FileField(upload_to='documentos/')
    certificado_eps = models.FileField(upload_to='documentos/')
    certificacion_residencia = models.FileField(upload_to='documentos/')
    consentimiento_informado = models.FileField(upload_to='documentos/')

    def __str__(self):
        return f"Documentos de {self.participante.nombre}"

    class Meta:
        db_table = 'formulario_documento_requisito'



