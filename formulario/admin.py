from django.contrib import admin
from .models import (
    Docente, Curso, Participante, Clase, Asistencia, ActividadCultura # ✅ Agregado
)

# ✅ Configuración de Participante en el Django Admin
class ParticipanteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'identificacion', 'correo', 'telefono', 'curso')  # ✅ Muestra estas columnas en la lista
    search_fields = ('nombre', 'identificacion', 'correo')  # ✅ Habilita la búsqueda rápida
    list_filter = ('curso',)  # ✅ Permite filtrar por curso
    ordering = ('nombre',)  # ✅ Ordena alfabéticamente por nombre

# ✅ Registro de otros modelos
admin.site.register(Docente)
admin.site.register(Curso)
admin.site.register(Participante)
admin.site.register(Clase)
admin.site.register(Asistencia)
admin.site.register(ActividadCultura)
