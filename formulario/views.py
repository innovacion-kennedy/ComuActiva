from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from collections import defaultdict
from django.db.models import Count

from .models import Proyecto, Participante, Curso, Docente, DatosComplementarios, CursoExtendido, Acudiente, Disciplina
from .forms import (
    ParticipanteForm, DocenteForm, DatosComplementariosForm, AcudienteForm,
    CursoExtendidoForm, DocumentoRequisitoForm, DisciplinaForm, SeleccionarCursoForm, CursoAsignacionForm, CursoExtendido
)

import openpyxl
from reportlab.pdfgen import canvas
from datetime import date, datetime
import json
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from io import BytesIO
from .onedrive_upload import subir_a_onedrive 

def convertir_a_serializable(data):
    serializable = {}
    for key, value in data.items():
        if isinstance(value, (date, datetime)):
            serializable[key] = value.isoformat()  # convierte a 'YYYY-MM-DD'
        else:
            serializable[key] = value
    return serializable


# ✅ Vista de la página de inicio
from .models import Participante

def home(request):
    try:
        participante = Participante.objects.latest('id')  # o cualquier lógica que prefieras
    except Participante.DoesNotExist:
        participante = None
    return render(request, 'formulario/index.html', {'participante': participante})



# ✅ Vista para listar proyectos
def lista_proyectos(request):
    proyectos = Proyecto.objects.all().values('id', 'nombre', 'descripcion', 'fecha_inicio', 'fecha_fin')
    return render(request, 'formulario/proyectos.html', {'proyectos': proyectos})

# ✅ Vista para manejar el formulario de participantes
def formulario_participante(request):
    form = ParticipanteForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            participante = form.save(commit=False)

            # ✅ Asignar curso desde sesión correctamente indentado
            curso_extendido_id = request.session.get('curso_extendido_id')
            if curso_extendido_id:
                participante.curso_extendido_id = curso_extendido_id
                del request.session['curso_extendido_id']

            # ✅ Calcular edad automáticamente
            if participante.fecha_nacimiento:
                hoy = date.today()
                participante.edad = hoy.year - participante.fecha_nacimiento.year - (
                    (hoy.month, hoy.day) < (participante.fecha_nacimiento.month, participante.fecha_nacimiento.day)
                )

            participante.save()

            # ✅ Redirigir a datos complementarios usando el ID del participante recién guardado
            messages.success(request, "✅ Participante registrado correctamente.")
            return redirect('datos_complementarios', participante_id=participante.id)

        else:
            messages.error(request, "❌ Corrige los errores.")

    # 👉 Esto se ejecuta si no es POST o si hubo errores
    return render(request, 'formulario/formulario_participante.html', {'form': form})




def formulario_docente(request):
    if request.method == 'POST':
        form = DocenteForm(request.POST)
        area_encargada = request.POST.get('area_encargada')
        disciplina = request.POST.get('disciplina')

        if form.is_valid():
            docente = form.save(commit=False)
            docente.area_encargada = area_encargada
            docente.disciplina = disciplina
            docente.save()
            messages.success(request, "✅ El docente ha sido registrado exitosamente.")
            return redirect('exito_docente')  # 👈 importante
        else:
            messages.error(request, "❌ Corrige los errores del formulario.")
    else:
        form = DocenteForm()

    return render(request, 'formulario/formulario_docente.html', {
        'form': form
    })


def exito_docente(request):
    return render(request, 'formulario/exito_docente.html')

# ✅ Vista de éxito después de un registro exitoso
def vista_exito(request):
    return render(request, 'formulario/exito.html')

# ✅ Nueva vista para consultar participantes con sus disciplinas y docentes

def consulta_participantes(request):
    filtro_nombre = request.GET.get('nombre', '').strip()
    filtro_identificacion = request.GET.get('identificacion', '').strip()
    filtro_disciplina = request.GET.get('disciplina', '').strip()
    filtro_profesor = request.GET.get('profesor', '').strip()

    # Filtrar solo participantes que tengan todos los datos obligatorios
    participantes = Participante.objects.select_related(
        'curso_extendido',
        'curso_extendido__disciplina',
        'curso_extendido__docente',
        'datos_complementarios'
    ).filter(
        datos_complementarios__isnull=False,
        curso_extendido__isnull=False,
        curso_extendido__disciplina__isnull=False,
        curso_extendido__disciplina__tipo__isnull=False,
        curso_extendido__docente__isnull=False,
        curso_extendido__horario__isnull=False,
        curso_extendido__lugar__isnull=False,
    )

    # Aplicar filtros si se usan
    if filtro_nombre:
        participantes = participantes.filter(nombre__icontains=filtro_nombre)
    if filtro_identificacion:
        participantes = participantes.filter(identificacion__icontains=filtro_identificacion)
    if filtro_disciplina:
        participantes = participantes.filter(curso_extendido__disciplina__nombre__icontains=filtro_disciplina)
    if filtro_profesor:
        participantes = participantes.filter(curso_extendido__docente__nombre__icontains=filtro_profesor)

    return render(request, 'formulario/consultas.html', {
        'participantes': participantes,
        'filtro_nombre': filtro_nombre,
        'filtro_identificacion': filtro_identificacion,
        'filtro_disciplina': filtro_disciplina,
        'filtro_profesor': filtro_profesor,
    })



def exportar_excel(request):
    participantes = Participante.objects.select_related(
        'curso_extendido__disciplina',
        'curso_extendido__docente'
    ).all()

    if not participantes.exists():
        messages.warning(request, "⚠️ No hay participantes para exportar.")
        return redirect('consulta_participantes')

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Participantes"

    # Encabezados
    ws.append([
        "Nombre", "Tipo Documento", "Identificación", "Edad", "Correo",
        "Teléfono", "Dirección", "Disciplina", "Tipo", "Docente",
        "Lugar", "Horario"
    ])

    # Datos
    for p in participantes:
        ws.append([
            p.nombre,
            p.tipo_documento,
            p.identificacion,
            p.edad,
            p.correo,
            p.telefono or "-",
            p.direccion or "-",
            p.curso_extendido.disciplina.nombre if p.curso_extendido and p.curso_extendido.disciplina else "-",
            p.curso_extendido.disciplina.get_tipo_display() if p.curso_extendido and p.curso_extendido.disciplina else "-",
            p.curso_extendido.docente.nombre if p.curso_extendido and p.curso_extendido.docente else "-",
            p.curso_extendido.lugar if p.curso_extendido and p.curso_extendido.lugar else "-",
            p.curso_extendido.horario if p.curso_extendido and p.curso_extendido.horario else "-",
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=participantes.xlsx'
    wb.save(response)
    return response


# ✅ Exportar a PDF con formato mejorado
def exportar_pdf(request):
    participantes = Participante.objects.select_related(
        'curso_extendido__disciplina',
        'curso_extendido__docente'
    ).all()

    if not participantes.exists():
        messages.warning(request, "⚠️ No hay participantes para exportar.")
        return redirect('consulta_participantes')

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=participantes.pdf'

    p = canvas.Canvas(response, pagesize=(800, 1000))
    p.setFont("Helvetica-Bold", 16)
    p.drawString(240, 970, "LISTA DE PARTICIPANTES")

    y = 940
    p.setFont("Helvetica-Bold", 10)
    headers = [
        "Nombre", "ID", "Edad", "Correo", "Teléfono",
        "Disciplina", "Tipo", "Docente", "Lugar", "Horario"
    ]
    for idx, header in enumerate(headers):
        p.drawString(50 + (idx * 70), y, header)

    y -= 20
    p.setFont("Helvetica", 8)

    for pte in participantes:
        if y < 50:
            p.showPage()
            y = 970
            p.setFont("Helvetica", 8)

        p.drawString(50, y, pte.nombre)
        p.drawString(120, y, pte.identificacion)
        p.drawString(190, y, str(pte.edad))
        p.drawString(220, y, (pte.correo or "")[:15])
        p.drawString(300, y, (pte.telefono or "")[:12])
        p.drawString(370, y, pte.curso_extendido.disciplina.nombre if pte.curso_extendido else "-")
        p.drawString(440, y, pte.curso_extendido.disciplina.get_tipo_display() if pte.curso_extendido else "-")
        p.drawString(510, y, pte.curso_extendido.docente.nombre if pte.curso_extendido else "-")
        p.drawString(580, y, pte.curso_extendido.lugar if pte.curso_extendido else "-")
        p.drawString(650, y, str(pte.curso_extendido.horario) if pte.curso_extendido and pte.curso_extendido.horario else "-")

        y -= 18

    p.showPage()
    p.save()
    return response


# ✅ Vista para datos complementarios
def formulario_multistep(request):
    paso = int(request.GET.get("paso", 0))
    total_pasos = 3

    if paso == 0:
        form = ParticipanteForm(request.POST or None)
        if request.method == "POST" and form.is_valid():
            datos = form.cleaned_data
            if datos.get('fecha_nacimiento'):
                datos['fecha_nacimiento'] = datos['fecha_nacimiento'].isoformat()
            request.session['form_participante'] = datos
            return redirect("?paso=1")

    elif paso == 1:
        form = DatosComplementariosForm(request.POST or None)
        if request.method == "POST" and form.is_valid():
            request.session['form_complementarios'] = form.cleaned_data
            return redirect("?paso=2")

    elif paso == 2:
        form = AcudienteForm(request.POST or None)
        if request.method == "POST" and form.is_valid():
            try:
                participante_data = request.session.get("form_participante")
                complementarios_data = request.session.get("form_complementarios")
                acudiente_data = form.cleaned_data

                if participante_data.get('fecha_nacimiento'):
                    participante_data['fecha_nacimiento'] = datetime.strptime(participante_data['fecha_nacimiento'], "%Y-%m-%d").date()
                    hoy = date.today()
                    participante_data['edad'] = hoy.year - participante_data['fecha_nacimiento'].year - (
                        (hoy.month, hoy.day) < (participante_data['fecha_nacimiento'].month, participante_data['fecha_nacimiento'].day)
                    )

                participante = Participante.objects.create(**participante_data)
                DatosComplementarios.objects.create(participante=participante, **complementarios_data)
                Acudiente.objects.create(participante=participante, **acudiente_data)

                for key in ['form_participante', 'form_complementarios']:
                    request.session.pop(key, None)

                messages.success(request, "✅ Inscripción completada correctamente.")
                return redirect("vista_exito")

            except Exception as e:
                messages.error(request, f"❌ Error: {e}")

    else:
        return redirect("?paso=0")

    return render(request, "formulario/formulario_multistep.html", {
        "form": form,
        "paso": paso,
        "total_pasos": total_pasos,
    })




# Vista de Datos Complementarios (Paso 1)
def datos_complementarios(request, participante_id):
    participante = get_object_or_404(Participante, id=participante_id)

    try:
        datos = participante.datos_complementarios
    except DatosComplementarios.DoesNotExist:
        datos = None

    if request.method == 'POST':
        form = DatosComplementariosForm(request.POST, instance=datos)
        if form.is_valid():
            datos_complementarios = form.save(commit=False)
            datos_complementarios.participante = participante
            datos_complementarios.save()
            form.save_m2m()  # Guardar campos many-to-many (nivel educativo)
            print("✅ GUARDADO:", datos_complementarios.__dict__)

            messages.success(request, '✅ Datos complementarios guardados correctamente.')
            return redirect('acudiente', participante_id=participante.id)
        else:
            messages.error(request, '❌ Por favor corrija los errores del formulario.')
    else:
        form = DatosComplementariosForm(instance=datos)

    return render(request, 'formulario/datos_complementarios.html', {
        'form': form,
        'participante': participante,
    })

# Vista para registrar al acudiente


def registrar_acudiente(request, participante_id):
    participante = get_object_or_404(Participante, id=participante_id)

    if request.method == "POST":
        form = AcudienteForm(request.POST)
        if form.is_valid():
            acudiente = form.save(commit=False)
            acudiente.participante = participante
            acudiente.save()
            return redirect("resumen_registro", participante_id=participante.id)
    else:
        form = AcudienteForm()

    return render(request, "formulario/datos_acudiente.html", {
        "form": form,
        "participante": participante
    })



# Vista para registrar curso

def lista_cursos_registrados(request):
    # Aquí puedes agregar la lógica para obtener los cursos registrados
    cursos = CursoExtendido.objects.all().order_by('-id')
    return render(request, 'formulario/lista_cursos.html', {'cursos': cursos})


# views.py


def formulario_curso(request):
    participante_id = request.session.get("participante_id")
    participante = get_object_or_404(Participante, id=participante_id)

    tipo_area = participante.curso_extendido.disciplina.tipo if participante.curso_extendido else None


    if request.method == "POST":
        form = CursoAsignacionForm(request.POST, tipo_area=tipo_area)
        if form.is_valid():
            curso = form.cleaned_data["curso"]
            participante.curso_extendido = curso

            participante.save()

            messages.success(request, "✅ ¡Curso asignado correctamente!")
            return redirect("resumen_registro", participante_id=participante.id)
    else:
        form = CursoAsignacionForm(tipo_area=tipo_area)

    return render(request, "formulario/formulario_curso.html", {
        "form": form,
        "participante": participante
    })


# views.py
def resumen_registro(request, participante_id):
    participante = get_object_or_404(Participante, id=participante_id)
    datos_complementarios = getattr(participante, 'datos_complementarios', None)
    acudiente = Acudiente.objects.filter(participante=participante).first()

    # 🔍 DEPURACIÓN TEMPORAL DETALLADA
    if datos_complementarios:
        print("\n💡 DATOS COMPLEMENTARIOS:")
        for field in [
            'identidad_genero', 'grupo_etnico', 'discapacidad',
            'tipo_discapacidad', 'tipo_sangre', 'nivel_educativo',
            'nombre_organizacion', 'otro_nivel_educativo'
        ]:
            valor = getattr(datos_complementarios, field, '---')
            if field == 'nivel_educativo':
                print(f"{field}: {[n.nombre for n in valor.all()]} (type: {type(valor)})")
            else:
                print(f"{field}: {valor} (type: {type(valor)})")
    else:
        print("🔴 No hay datos complementarios para este participante.")

    tipo_area = None
    if participante.curso_extendido and participante.curso_extendido.disciplina:
        tipo_area = participante.curso_extendido.disciplina.tipo

    if request.method == 'POST':
        form = CursoAsignacionForm(request.POST, tipo_area=tipo_area)
        if form.is_valid():
            curso = form.cleaned_data['curso']
            participante.curso_extendido = curso
            participante.save()
            return redirect('resumen_registro', participante_id=participante.id)
    else:
        form = CursoAsignacionForm(tipo_area=tipo_area)

    return render(request, 'formulario/resumen_registro.html', {
        'participante': participante,
        'datos_complementarios': datos_complementarios,
        'acudiente': acudiente,
        'form': form,
    })
def cargue_documento(request, participante_id):
    participante = get_object_or_404(Participante, id=participante_id)

    if request.method == 'POST':
        form = DocumentoRequisitoForm(request.POST, request.FILES)
        if form.is_valid():
            documento = form.save(commit=False)
            documento.participante = participante
            documento.save()

            # Lista de campos de archivo
            campos_archivos = [
                'formulario_inscripcion_firmado',
                'documento_identidad',
                'certificado_eps',
                'certificacion_residencia',
                'consentimiento_informado'
            ]

            for campo in campos_archivos:
                archivo = request.FILES.get(campo)
                if archivo:
                    nombre_archivo = f"{participante.nombre}_{campo}_{archivo.name}"
                    contenido = archivo.read()

                    # Subida a OneDrive
                    exito, mensaje = subir_a_onedrive(nombre_archivo, contenido)
                    print(f"📤 Subida de {campo}: {mensaje}")
                    if exito:
                        messages.success(request, f"✅ {campo.replace('_', ' ').capitalize()}: subido correctamente.")
                    else:
                        messages.warning(request, f"⚠️ {campo.replace('_', ' ').capitalize()}: error al subir. {mensaje}")
                else:
                    print(f"📎 {campo} no se adjuntó.")

            return redirect('consulta_participantes')
        else:
            messages.error(request, "❌ Corrige los errores antes de continuar.")
    else:
        form = DocumentoRequisitoForm()

    return render(request, 'formulario/requisitos.html', {
        'form': form,
        'participante': participante
    })




def crear_curso(request):
    if request.method == 'POST':
        form = CursoExtendidoForm(request.POST)
        if form.is_valid():
            curso = form.save()
            messages.success(request, "✅ Curso creado correctamente.")
            return redirect('lista_cursos')
        else:
            messages.error(request, "❌ Corrige los errores antes de continuar.")
    else:
        form = CursoExtendidoForm()

    return render(request, 'formulario/cursoscreados.html', {'form': form})



def crear_disciplina(request):
    if request.method == 'POST':
        form = DisciplinaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Disciplina creada correctamente.")
            return redirect('crear_curso')
        else:
            messages.error(request, "❌ Corrige los errores del formulario.")
    else:
        form = DisciplinaForm()

    return render(request, 'formulario/crear_disciplina.html', {'form': form})


@csrf_exempt
def crear_disciplina_ajax(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            nombre = data.get('nombre')
            tipo = data.get('tipo')

            if not nombre or not tipo:
                return JsonResponse({'error': 'Nombre y tipo son obligatorios.'}, status=400)

            if Disciplina.objects.filter(nombre__iexact=nombre.strip(), tipo=tipo).exists():
                return JsonResponse({'error': 'Ya existe una disciplina con ese nombre y tipo.'}, status=400)

            disciplina = Disciplina.objects.create(
                nombre=nombre.strip().capitalize(),
                tipo=tipo
            )

            return JsonResponse({
                'success': True,
                'id': disciplina.id,
                'nombre': disciplina.nombre,
                'tipo': disciplina.tipo,
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método no permitido'}, status=405)





def obtener_disciplinas_por_tipo(request):
    tipo = request.GET.get("tipo")
    disciplinas = Disciplina.objects.filter(tipo=tipo).values("id", "nombre")
    return JsonResponse(list(disciplinas), safe=False)


def descargar_resumen_pdf(request, participante_id):
    participante = get_object_or_404(Participante, id=participante_id)
    datos_complementarios = getattr(participante, 'datos_complementarios', None)
    acudiente = getattr(participante, 'acudiente', None)

    html = render_to_string("formulario/pdf_resumen.html", {
        'participante': participante,
        'datos_complementarios': datos_complementarios,
        'acudiente': acudiente,
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="resumen_{participante.identificacion}.pdf"'
    pisa.CreatePDF(BytesIO(html.encode("UTF-8")), dest=response)
    return response




def reporte_inscritos(request):
    cursos = (
        Participante.objects
        .filter(curso_extendido__isnull=False)  # ✅ Solo con curso asignado
        .select_related("curso_extendido__disciplina", "curso_extendido__docente")
        .values(
            "curso_extendido__id",
            "curso_extendido__horario",
            "curso_extendido__lugar",
            "curso_extendido__disciplina__nombre",
            "curso_extendido__disciplina__tipo",
            "curso_extendido__docente__nombre",
        )
        .annotate(num_inscritos=Count("id"))
        .order_by("curso_extendido__disciplina__tipo", "curso_extendido__disciplina__nombre")
    )

    return render(request, 'formulario/reporte_inscritos.html', {
        'cursos': cursos
    })
