
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse
from .models import Proyecto, Participante, Curso, Docente, DatosComplementarios, CursoExtendido
from .forms import ParticipanteForm, DocenteForm, DatosComplementariosForm, AcudienteForm, CursoExtendidoForm, DocumentoRequisitoForm
import openpyxl  # Exportar a Excel
from reportlab.pdfgen import canvas  # Exportar a PDF
from datetime import date, datetime

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

            # Asignar curso desde sesión
            curso_id = request.session.get('curso_id')
            if curso_id:
                participante.curso_id = curso_id

            # Calcular edad
            if participante.fecha_nacimiento:
                hoy = date.today()
                participante.edad = hoy.year - participante.fecha_nacimiento.year - (
                    (hoy.month, hoy.day) < (participante.fecha_nacimiento.month, participante.fecha_nacimiento.day)
                )

            participante.save()
            messages.success(request, "✅ Participante registrado")
            return redirect('formulario_participante')
        else:
            messages.error(request, "❌ Corrige los errores.")

    return render(request, 'formulario/formulario_participante.html', {'form': form})



# ✅ Vista para manejar el formulario de docentes con radios dinámicos
def formulario_docente(request):
    mensaje_exito = False

    if request.method == 'POST':
        form = DocenteForm(request.POST)
        area_encargada = request.POST.get('area_encargada')
        disciplina = request.POST.get('disciplina')
        if form.is_valid():
            docente = form.save(commit=False)
            docente.area_encargada = area_encargada
            docente.save()
            form.save_m2m()
            mensaje_exito = True
            form = DocenteForm()
        else:
            messages.error(request, "❌ Corrige los errores del formulario.")
    else:
        form = DocenteForm()

    return render(request, 'formulario/formulario_docente.html', {
        'form': form,
        'mensaje_exito': mensaje_exito,
    })


# ✅ Vista de éxito después de un registro exitoso
def vista_exito(request):
    return render(request, 'formulario/exito.html')

# ✅ Nueva vista para consultar participantes con sus disciplinas y docentes

def consulta_participantes(request):
    filtro_nombre = request.GET.get('nombre', '').strip()
    filtro_identificacion = request.GET.get('identificacion', '').strip()
    filtro_disciplina = request.GET.get('disciplina', '').strip()
    filtro_profesor = request.GET.get('profesor', '').strip()

    participantes = Participante.objects.select_related('curso').all()

    if filtro_nombre:
        participantes = participantes.filter(nombre__icontains=filtro_nombre)
    if filtro_identificacion:
        participantes = participantes.filter(identificacion__icontains=filtro_identificacion)
    if filtro_disciplina:
        participantes = participantes.filter(curso__nombre__icontains=filtro_disciplina)
    if filtro_profesor:
        docentes = Docente.objects.filter(nombre__icontains=filtro_profesor)
        cursos_docente = Curso.objects.filter(docente__in=docentes)
        participantes = participantes.filter(curso__in=cursos_docente)

    return render(request, 'formulario/consultas.html', {
        'participantes': participantes,
        'filtro_nombre': filtro_nombre,
        'filtro_identificacion': filtro_identificacion,
        'filtro_disciplina': filtro_disciplina,
        'filtro_profesor': filtro_profesor,
    })


# ✅ Exportar a Excel
def exportar_excel(request):
    participantes = Participante.objects.all()

    if not participantes.exists():
        messages.warning(request, "⚠️ No hay participantes para exportar.")
        return redirect('consulta_participantes')

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Participantes"

    ws.append(["Nombre", "Tipo Documento", "Identificación", "Fecha Expedición", "Edad", "Correo", "Teléfono", "Dirección", "Disciplina", "Profesor Asignado"])

    for participante in participantes:
        docentes = ", ".join([docente.nombre for docente in participante.curso.docente_set.all()])
        ws.append([
            participante.nombre,
            participante.tipo_documento,
            participante.identificacion,
            participante.fecha_expedicion,
            participante.edad,
            participante.correo,
            participante.telefono,
            participante.direccion,
            participante.curso.nombre if participante.curso else "Sin curso",
            docentes if docentes else "Sin docentes"
        ])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=participantes.xlsx'
    wb.save(response)
    return response

# ✅ Exportar a PDF con formato mejorado
def exportar_pdf(request):
    participantes = Participante.objects.all()

    if not participantes.exists():
        messages.warning(request, "⚠️ No hay participantes para exportar.")
        return redirect('consulta_participantes')

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=participantes.pdf'

    p = canvas.Canvas(response)
    p.setFont("Helvetica-Bold", 14)
    p.drawString(200, 800, "Lista de Participantes")
    p.setFont("Helvetica", 10)

    y = 780

    for participante in participantes:
        docentes = ", ".join([docente.nombre for docente in participante.curso.docente_set.all()])
        texto = f"{participante.nombre} | {participante.tipo_documento} | {participante.identificacion} | {participante.fecha_expedicion} | {participante.edad} | {participante.correo} | {participante.telefono} | {participante.direccion} | {participante.curso.nombre if participante.curso else 'Sin curso'} | {docentes if docentes else 'Sin docentes'}"

        max_chars_per_line = 120
        lines = [texto[i:i+max_chars_per_line] for i in range(0, len(texto), max_chars_per_line)]

        for line in lines:
            p.drawString(50, y, line)
            y -= 20

        y -= 10

        if y < 50:
            p.showPage()
            p.setFont("Helvetica", 10)
            y = 780

    p.showPage()
    p.save()
    return response

# ✅ Vista para datos complementarios
def formulario_multistep(request):
    paso = int(request.GET.get("paso", 0))
    total_pasos = 4

    # Paso 0: Participante
    if paso == 0:
        form = ParticipanteForm(request.POST or None)
        if request.method == "POST" and form.is_valid():
            # Convertir fechas a string antes de guardar en la sesión
            form_data = form.cleaned_data
            if form_data.get('fecha_nacimiento'):
                form_data['fecha_nacimiento'] = form_data['fecha_nacimiento'].isoformat()  # Convertir fecha a string
            request.session["form_data_participante"] = form_data
            return redirect("?paso=1")

    # Paso 1: Datos complementarios
    elif paso == 1:
        form = DatosComplementariosForm(request.POST or None)
        if request.method == "POST" and form.is_valid():
            form_data = form.cleaned_data
            request.session["form_data_complementarios"] = form_data
            return redirect("?paso=2")

    # Paso 2: Acudiente
    elif paso == 2:
        form = AcudienteForm(request.POST or None)
        if request.method == "POST" and form.is_valid():
            form_data = form.cleaned_data
            request.session["form_data_acudiente"] = form_data
            return redirect("?paso=3")

    # Paso 3: Curso
    elif paso == 3:
        form = CursoExtendidoForm(request.POST or None)
        if request.method == "POST" and form.is_valid():
            try:
                curso = form.save()
                messages.success(request, "✅ Curso registrado correctamente.")  # Mensaje agregado

                # Recuperar datos anteriores y convertir las fechas de nuevo a objetos date
                participante_data = request.session.get("form_data_participante")
                if participante_data and participante_data.get('fecha_nacimiento'):
                    participante_data['fecha_nacimiento'] = datetime.strptime(participante_data['fecha_nacimiento'], "%Y-%m-%d").date()

                complementarios_data = request.session.get("form_data_complementarios")
                acudiente_data = request.session.get("form_data_acudiente")

                # Crear participante y asociar curso
                participante = Participante(**participante_data)
                participante.curso = curso
                if participante.fecha_nacimiento:
                    hoy = date.today()
                    participante.edad = hoy.year - participante.fecha_nacimiento.year - (
                        (hoy.month, hoy.day) < (participante.fecha_nacimiento.month, participante.fecha_nacimiento.day)
                    )
                participante.save()

                # Crear relacionados
                DatosComplementarios.objects.create(participante=participante, **complementarios_data)
                Acudiente.objects.create(participante=participante, **acudiente_data)

                # Limpiar sesión
                for key in ["form_data_participante", "form_data_complementarios", "form_data_acudiente"]:
                    if key in request.session:
                        del request.session[key]

                return redirect("formulario_multistep?paso=3")  # redirigir al mismo paso para mostrar mensaje

            except Exception as e:
                messages.error(request, f"Ocurrió un error al guardar los datos: {e}")

    context = {
        "form": form,
        "paso": paso,
        "total_pasos": total_pasos,
    }
    return render(request, "formulario/formulario_multistep.html", context)



# Vista de Datos Complementarios (Paso 1)
def datos_complementarios(request):
    if request.method == 'POST':
        form = DatosComplementariosForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('formulario_participante')
    else:
        form = DatosComplementariosForm()
    return render(request, 'formulario/datos_complementarios.html', {'form': form})

# Vista para registrar al acudiente
def registrar_acudiente(request):
    if request.method == "POST":
        form = AcudienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "¡El acudiente ha sido registrado exitosamente!")
            return redirect('datos_complementarios')  # O la vista que desees redirigir
        else:
            messages.error(request, "Corrige los errores antes de continuar.")
    else:
        form = AcudienteForm()

    return render(request, "formulario/datos_acudiente.html", {"form": form})

# Vista para registrar curso

def lista_cursos_registrados(request):
    # Aquí puedes agregar la lógica para obtener los cursos registrados
    cursos = CursoExtendido.objects.all().order_by('-id')
    return render(request, 'formulario/lista_cursos.html', {'cursos': cursos})


def formulario_curso(request):
    if request.method == 'POST':
        form = CursoExtendidoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Curso registrado correctamente.")
            return redirect('formulario_participante')  # O la vista a la que deseas redirigir
        else:
            messages.error(request, "Corrige los errores.")
    else:
        form = CursoExtendidoForm()

    return render(request, 'formulario/formulario_curso.html', {'form': form})

from django.shortcuts import render, get_object_or_404
from .models import Participante
from .forms import DocumentoRequisitoForm

def cargue_documento(request, participante_id):
    # Obtén el participante por su ID
    participante = get_object_or_404(Participante, id=participante_id)

    # Si se recibe el formulario con archivos
    if request.method == 'POST':
        form = DocumentoRequisitoForm(request.POST, request.FILES)
        if form.is_valid():
            # Guarda el documento relacionado con el participante
            documento = form.save(commit=False)
            documento.participante = participante  # Asocia el documento con el participante
            documento.save()  # Guarda el documento en la base de datos
            messages.success(request, "✅ Documento cargado correctamente.")
            return redirect('consulta_participantes')  # O la vista que quieras redirigir después
        else:
            messages.error(request, "❌ Corrige los errores antes de continuar.")
    else:
        form = DocumentoRequisitoForm()

    return render(request, 'formulario/cargue_documento.html', {'form': form, 'participante': participante})
