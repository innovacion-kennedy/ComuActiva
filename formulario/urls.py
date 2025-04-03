from django.urls import path
from django.views.generic import TemplateView
from . import views
from .views import (
    exportar_excel,
    exportar_pdf,
    datos_complementarios,
    registrar_acudiente,
    formulario_docente,
    formulario_participante,
    formulario_curso,
    lista_proyectos,
    lista_cursos_registrados,
    consulta_participantes,
    vista_exito,
    home,
    cargue_documento,
    crear_disciplina,
    crear_disciplina_ajax,
    obtener_disciplinas_por_tipo,
    crear_curso,
)

urlpatterns = [
    path('', home, name='home'),
    path('index/', home, name='index'),

    # Formularios de inscripción
    path('formulario_participante/', formulario_participante, name='formulario_participante'),
    path('datos_complementarios/<int:participante_id>/', datos_complementarios, name='datos_complementarios'),
    path('acudiente/<int:participante_id>/', registrar_acudiente, name='acudiente'),
    path('formulario_docente/', formulario_docente, name='formulario_docente'),
    path('formulario-curso/', formulario_curso, name='formulario_curso'),

    # Gestión de cursos y disciplinas
    path('crear-disciplina/', crear_disciplina, name='crear_disciplina'),
    path('ajax/crear-disciplina/', crear_disciplina_ajax, name='crear_disciplina_ajax'),
    path('ajax/disciplinas/', obtener_disciplinas_por_tipo, name='obtener_disciplinas_por_tipo'),
    path('crear-curso/', crear_curso, name='crear_curso'),  # Vista de gestión
    path('nuevo-curso/', crear_curso, name='crear_curso_nuevo'),  # Vista para usuarios

    # Listados y reportes
    path('lista-cursos/', lista_cursos_registrados, name='lista_cursos'),
    path('proyectos/', lista_proyectos, name='lista_proyectos'),
    path('consultas/', consulta_participantes, name='consulta_participantes'),

    # Exportación
    path('exportar-excel/', exportar_excel, name='exportar_excel'),
    path('exportar-pdf/', exportar_pdf, name='exportar_pdf'),

    # Archivos y resumen
    path('cargue-documento/<int:participante_id>/', cargue_documento, name='cargue_documento'),
    path('resumen-registro/<int:participante_id>/', views.resumen_registro, name='resumen_registro'),
    path('descargar-resumen/<int:participante_id>/', views.descargar_resumen_pdf, name='descargar_resumen_pdf'),

    # Vistas de éxito
    path('exito/', vista_exito, name='vista_exito'),
    path('exito-docente/', views.exito_docente, name='exito_docente'),
    path('registro-exitoso-docente/', TemplateView.as_view(template_name='formulario/exito_docente.html'), name='exito_docente'),

    # Indicadores
    path('reporte-inscritos/', views.reporte_inscritos, name='reporte_inscritos'),
]
