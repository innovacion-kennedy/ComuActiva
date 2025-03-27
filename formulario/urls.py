from django.urls import path
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
    formulario_multistep,
    formulario_curso, 

)

urlpatterns = [
    path('', home, name='home'),
    path('proyectos/', lista_proyectos, name='lista_proyectos'),
    path('formulario-curso/', formulario_curso, name='formulario_curso'),
    path('lista-cursos/', lista_cursos_registrados, name='lista_cursos'),
    path('formulario_participante/', formulario_participante, name='formulario_participante'),
    path('datos_complementarios/', datos_complementarios, name='datos_complementarios'),
    path('acudiente/', registrar_acudiente, name='registrar_acudiente'),
    path('formulario_docente/', formulario_docente, name='formulario_docente'),
    path('exito/', vista_exito, name='vista_exito'),
    path('consultas/', consulta_participantes, name='consulta_participantes'),
    path('exportar-excel/', exportar_excel, name='exportar_excel'),
    path('exportar-pdf/', exportar_pdf, name='exportar_pdf'),
    path('cargue-documento/<int:participante_id>/', cargue_documento, name='cargue_documento'),  # Corregido aquí
    path('formulario-curso/', formulario_curso, name='formulario_curso'),


    # ✅ Nueva ruta para formulario multistep
    path('formulario-multistep/', formulario_multistep, name='formulario_multistep'),
]
