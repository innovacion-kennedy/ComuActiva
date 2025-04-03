from django.contrib import admin 
from .models import (
    Docente, Curso, Participante, Clase, Asistencia, ActividadCultura,
    CursoExtendido, DatosComplementarios, Acudiente, Proyecto, NivelEducativo,
    DocumentoRequisito, Disciplina
)

# ✅ Participante
class ParticipanteAdmin(admin.ModelAdmin):
    list_display = (
        'nombre', 'tipo_documento', 'identificacion', 'fecha_expedicion', 'lugar_expedicion',
        'pais_origen', 'ciudad', 'area', 'localidad', 'barrio', 'correo', 'telefono',
        'direccion', 'fecha_nacimiento', 'edad', 'curso', 'curso_extendido'
    )
    search_fields = ('nombre', 'identificacion', 'correo')
    list_filter = ('curso', 'curso_extendido', 'area', 'ciudad')
    ordering = ('nombre',)

# ✅ Curso
class CursoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)
    ordering = ('nombre',)

# ✅ Docente
class DocenteAdmin(admin.ModelAdmin):
    list_display = (
        'nombre', 'identificacion', 'correo', 'telefono', 'direccion',
        'fecha_nacimiento', 'area_encargada', 'disciplina',
    )
    search_fields = ('nombre', 'identificacion', 'correo')
    list_filter = ('area_encargada', 'disciplina')

# ✅ Clase
class ClaseAdmin(admin.ModelAdmin):
    list_display = ('curso', 'docente', 'fecha_clase', 'cupo_maximo', 'cupo_actual')

# ✅ Asistencia
class AsistenciaAdmin(admin.ModelAdmin):
    list_display = ('alumno', 'clase', 'fecha_asistencia')

# ✅ Curso Extendido
class CursoExtendidoAdmin(admin.ModelAdmin):
    list_display = ('tipo_curso', 'disciplina', 'horario', 'lugar', 'docente')
    search_fields = ('disciplina',)
    list_filter = ('tipo_curso', 'lugar')

# ✅ Datos Complementarios (extendido)
class DatosComplementariosAdmin(admin.ModelAdmin):
    list_display = (
        'participante', 'identidad_genero', 'grupo_etnico', 'discapacidad',
        'tipo_discapacidad', 'enfermedad_huerfana', 'conflicto_armado',
        'tipo_sangre', 'mostrar_niveles_educativos'
    )
    list_filter = ('grupo_etnico', 'discapacidad', 'tipo_sangre')

    def mostrar_niveles_educativos(self, obj):
        return ", ".join([ne.nombre for ne in obj.nivel_educativo.all()])
    mostrar_niveles_educativos.short_description = 'Nivel educativo'

# ✅ Acudiente
class AcudienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono','ocupacion', 'parentesco', 'participante')

# ✅ Proyecto
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha_inicio', 'fecha_fin')

# ✅ Nivel Educativo
class NivelEducativoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

# ✅ Documentos Requisitos
class DocumentoRequisitoAdmin(admin.ModelAdmin):
    list_display = ('participante',)
    search_fields = ('participante__nombre',)
    list_filter = ('participante__curso_extendido__disciplina',)

# ✅ Actividad Cultural
class ActividadCulturaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)


@admin.register(Disciplina)
class DisciplinaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo')
    list_filter = ('tipo',)
    search_fields = ('nombre',)


# ✅ Registro de modelos
admin.site.register(Docente, DocenteAdmin)
admin.site.register(Curso, CursoAdmin)
admin.site.register(Participante, ParticipanteAdmin)
admin.site.register(Clase, ClaseAdmin)
admin.site.register(Asistencia, AsistenciaAdmin)
admin.site.register(ActividadCultura, ActividadCulturaAdmin)
admin.site.register(CursoExtendido, CursoExtendidoAdmin)
admin.site.register(DatosComplementarios, DatosComplementariosAdmin)
admin.site.register(Acudiente, AcudienteAdmin)
admin.site.register(Proyecto, ProyectoAdmin)
admin.site.register(NivelEducativo, NivelEducativoAdmin)
admin.site.register(DocumentoRequisito, DocumentoRequisitoAdmin)

