from django import forms
from django.core.exceptions import ValidationError
from .models import Participante, Curso, Docente, DatosComplementarios, Acudiente, CursoExtendido, DocumentoRequisito, NivelEducativo, Disciplina
from datetime import date
from .choices import TIPO_AREA_CHOICES, DISCIPLINAS_CULTURA, DISCIPLINAS_DEPORTE, DISCAPACIDAD_BOOLEAN_CHOICES, TIPOS_DISCAPACIDAD 

# ✅ Opciones de zona geográfica
ZONA_GEOGRAFICA_CHOICES = [
    ('Rural', 'Rural'),
    ('Urbano', 'Urbano'),
]   
    
# ✅ Opciones de áreas temáticas


BARRIO_CHOICES = [
    ('agrupacion pio x', 'agrupacion pio x'),
    ('agrupacion multifamiliar villa emilia', 'agrupacion multifamiliar villa emilia'),
    ('alferez real', 'alferez real'),
    ('americas central', 'americas central'),
    ('americas occidental i. ii y iii etapa', 'americas occidental i. ii y iii etapa'),
    ('antiguo hipodromo de techo ii etapa', 'antiguo hipodromo de techo ii etapa'),
    ('carvajal ii sector', 'carvajal ii sector'),
    ('centroamericas', 'centroamericas'),
    ('ciudad kennedy', 'ciudad kennedy'),
    ('conjunto res. el rincon de mandalay', 'conjunto res. el rincon de mandalay'),
    ('floresta sur', 'floresta sur'),
    ('fundadores', 'fundadores'),
    ('glorieta de las americas', 'glorieta de las americas'),
    ('hipotecho', 'hipotecho'),
    ('igualdad i sector', 'igualdad i sector'),
    ('igualdad ii sector', 'igualdad ii sector'),
    ('la floresta', 'la floresta'),
    ('la igualdad', 'la igualdad'),
    ('la llanura', 'la llanura'),
    ('la llanura manzana p', 'la llanura manzana p'),
    ('las americas', 'las americas'),
    ('las americas sector galan', 'las americas sector galan'),
    ('los sauces', 'los sauces'),
    ('mandalay etapa a sector ii', 'mandalay etapa a sector ii'),
    ('mandalay i sector', 'mandalay i sector'),
    ('marsella iii sector', 'marsella iii sector'),
    ('multifamiliares villa adriana mz. h', 'multifamiliares villa adriana mz. h'),
    ('nueva marsella i. ii y iii sector', 'nueva marsella i. ii y iii sector'),
    ('provivienda oriental', 'provivienda oriental'),
    ('santa rosa de carvajal', 'santa rosa de carvajal'),
    ('urb. los laureles (sauces-robles)', 'urb. los laureles (sauces-robles)'),
    ('villa adriana', 'villa adriana'),
    ('villa claudia', 'villa claudia'),
    ('urbanizacion castilla la nueva', 'urbanizacion castilla la nueva'),
]


# ✅ Lista de países optimizada
PAIS_CHOICES = [
    ('Afganistán', 'Afganistán'), ('Albania', 'Albania'), ('Alemania', 'Alemania'),
    ('Andorra', 'Andorra'), ('Angola', 'Angola'), ('Antigua y Barbuda', 'Antigua y Barbuda'),
    ('Arabia Saudita', 'Arabia Saudita'), ('Argelia', 'Argelia'), ('Argentina', 'Argentina'),
    ('Armenia', 'Armenia'), ('Australia', 'Australia'), ('Austria', 'Austria'),
    ('Brasil', 'Brasil'), ('Canadá', 'Canadá'), ('Colombia', 'Colombia'),
    ('Estados Unidos', 'Estados Unidos'), ('Francia', 'Francia'), ('Micronesia', 'Micronesia'),
    ('Moldavia', 'Moldavia'), ('Mónaco', 'Mónaco'), ('Mongolia', 'Mongolia'),
    ('Montenegro', 'Montenegro'), ('Mozambique', 'Mozambique'), ('Namibia', 'Namibia'),
    ('Nauru', 'Nauru'), ('Nepal', 'Nepal'), ('Nicaragua', 'Nicaragua'), ('Níger', 'Níger'),
    ('Nigeria', 'Nigeria'), ('Noruega', 'Noruega'), ('Nueva Zelanda', 'Nueva Zelanda'),
    ('Omán', 'Omán'), ('Pakistán', 'Pakistán'), ('Palaos', 'Palaos'), ('Panamá', 'Panamá'),
    ('Papúa Nueva Guinea', 'Papúa Nueva Guinea'), ('Paraguay', 'Paraguay'),
    ('Países Bajos', 'Países Bajos'), ('Perú', 'Perú'), ('Polonia', 'Polonia'),
    ('Portugal', 'Portugal'), ('Reino Unido', 'Reino Unido'),
    ('República Centroafricana', 'República Centroafricana'),
    ('República Checa', 'República Checa'), ('República Democrática del Congo', 'República Democrática del Congo'),
    ('República Dominicana', 'República Dominicana'), ('República del Congo', 'República del Congo'),
    ('Ruanda', 'Ruanda'), ('Rumanía', 'Rumanía'), ('Rusia', 'Rusia'), ('Samoa', 'Samoa'),
    ('San Cristóbal y Nieves', 'San Cristóbal y Nieves'), ('San Marino', 'San Marino'),
    ('San Vicente y las Granadinas', 'San Vicente y las Granadinas'), ('Santa Lucía', 'Santa Lucía'),
    ('Santo Tomé y Príncipe', 'Santo Tomé y Príncipe'), ('Senegal', 'Senegal'), ('Serbia', 'Serbia'),
    ('Seychelles', 'Seychelles'), ('Sierra Leona', 'Sierra Leona'), ('Singapur', 'Singapur'),
    ('Siria', 'Siria'), ('Somalia', 'Somalia'), ('Sri Lanka', 'Sri Lanka'), ('Suazilandia', 'Suazilandia'),
    ('Sudáfrica', 'Sudáfrica'), ('Sudán', 'Sudán'), ('Sudán del Sur', 'Sudán del Sur'),
    ('Suecia', 'Suecia'), ('Suiza', 'Suiza'), ('Surinam', 'Surinam'), ('Tailandia', 'Tailandia'),
    ('Tanzania', 'Tanzania'), ('Tayikistán', 'Tayikistán'), ('Timor Oriental', 'Timor Oriental'),
    ('Togo', 'Togo'), ('Tonga', 'Tonga'), ('Trinidad y Tobago', 'Trinidad y Tobago'),
    ('Túnez', 'Túnez'), ('Turkmenistán', 'Turkmenistán'), ('Turquía', 'Turquía'),
    ('Tuvalu', 'Tuvalu'), ('Ucrania', 'Ucrania'), ('Uganda', 'Uganda'), ('Uruguay', 'Uruguay'),
    ('Uzbekistán', 'Uzbekistán'), ('Vanuatu', 'Vanuatu'), ('Venezuela', 'Venezuela'),
    ('Vietnam', 'Vietnam'), ('Yemen', 'Yemen'), ('Yibuti', 'Yibuti'), ('Zambia', 'Zambia'),
    ('Zimbabue', 'Zimbabue')
]

# ✅ Formulario para Participantes
class ParticipanteForm(forms.ModelForm):
    TIPO_DOCUMENTO_CHOICES = [
        ('CC', 'Cédula de Ciudadanía'),
        ('TI', 'Tarjeta de Identidad'),
        ('CE', 'Cédula de Extranjería'),
    ]

    tipo_documento = forms.ChoiceField(choices=TIPO_DOCUMENTO_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    fecha_expedicion = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    lugar_expedicion = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    pais_origen = forms.ChoiceField(choices=PAIS_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    ciudad = forms.CharField(initial="Bogotá", widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    area = forms.ChoiceField(choices=ZONA_GEOGRAFICA_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    localidad = forms.CharField(initial="Kennedy", widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    barrio = forms.ChoiceField(choices=BARRIO_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    edad = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    curso_extendido = forms.ModelChoiceField(queryset=CursoExtendido.objects.all(), required=False, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Participante
        fields = ['nombre', 'tipo_documento', 'identificacion', 'fecha_expedicion', 'lugar_expedicion', 'pais_origen', 'ciudad', 'area', 'localidad', 'barrio', 'edad', 'correo', 'telefono', 'direccion', 'fecha_nacimiento', 'curso_extendido']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'identificacion': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
        }

    def clean_fecha_nacimiento(self):
        fecha_nacimiento = self.cleaned_data.get('fecha_nacimiento')
        if fecha_nacimiento:
            hoy = date.today()
            edad_calculada = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
            if edad_calculada < 0:
                raise ValidationError("La fecha de nacimiento no puede ser futura.")
        return fecha_nacimiento

    def clean_identificacion(self):
        identificacion = self.cleaned_data.get('identificacion')
        if len(identificacion) > 30:
            raise ValidationError("El número de identificación no puede tener más de 30 caracteres.")
        if Participante.objects.filter(identificacion=identificacion).exists():
            raise ValidationError("El número de identificación ya está registrado.")
        return identificacion

    def clean_correo(self):
        correo = self.cleaned_data.get('correo')
        if Participante.objects.filter(correo=correo).exists():
            raise ValidationError("El correo electrónico ya está registrado.")
        return correo


# ✅ Formulario para el registro de Docentes


DISCIPLINAS_DEPORTE = [
    ('Microfutbol', 'Microfutbol'),
    ('Futbol', 'Fútbol'),
    ('Basketball', 'Baloncesto'),
    ('Voleibol', 'Voleibol'),
]

DISCIPLINAS_CULTURA = [
    ('Danza', 'Danza'),
    ('Baile', 'Baile'),
    ('Fotografía', 'Fotografía'),
    ('Pintura', 'Pintura'),
]

TIPO_AREA_CHOICES = [
    ('Deporte', 'Deporte'),
    ('Cultura', 'Cultura'),
]

class DocenteForm(forms.ModelForm):
    area_encargada = forms.ChoiceField(
        choices=TIPO_AREA_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    disciplina = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )

    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        }),
        input_formats=['%Y-%m-%d'],
        required=True
    )

    class Meta:
        model = Docente
        fields = [
            'nombre', 'identificacion', 'correo', 'telefono', 'direccion',
            'fecha_nacimiento', 'area_encargada', 'disciplina'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo'}),
            'identificacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Identificación'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección'}),
        }

    def clean_identificacion(self):
        identificacion = self.cleaned_data.get('identificacion')
        if len(identificacion) > 30:
            raise ValidationError("El número de identificación no puede tener más de 30 caracteres.")
        if Docente.objects.filter(identificacion=identificacion).exists():
            raise ValidationError("El número de identificación ya está registrado.")
        return identificacion

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono and len(telefono) > 20:
            raise ValidationError("El número de teléfono no puede tener más de 20 caracteres.")
        return telefono
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        area = self.data.get('area_encargada') or self.initial.get('area_encargada')

        if area == 'Deporte':
            self.fields['disciplina'].choices = DISCIPLINAS_DEPORTE
        elif area == 'Cultura':
            self.fields['disciplina'].choices = DISCIPLINAS_CULTURA
        else:
            self.fields['disciplina'].choices = []


# ✅ Campo tipo de discapacidad (opcional)
  # ✅ Formulario para Datos Complementarios
class DatosComplementariosForm(forms.ModelForm):
    discapacidad = forms.ChoiceField(choices=DISCAPACIDAD_BOOLEAN_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}), label="¿Posee alguna discapacidad?")
    tipo_discapacidad = forms.ChoiceField(choices=TIPOS_DISCAPACIDAD, widget=forms.Select(attrs={'class': 'form-select'}), required=False)
    nivel_educativo = forms.ModelMultipleChoiceField(queryset=NivelEducativo.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)

    class Meta:
        model = DatosComplementarios
        fields = [
            'identidad_genero', 'grupo_etnico', 'discapacidad', 'tipo_discapacidad',
            'enfermedad_huerfana', 'enfermedad_nombre', 'conflicto_armado',
            'tipo_sangre', 'nivel_educativo', 'otro_nivel_educativo',
            'pertenece_organizacion', 'nombre_organizacion'
        ]
        widgets = {
            'identidad_genero': forms.Select(attrs={'class': 'form-select'}),
            'grupo_etnico': forms.Select(attrs={'class': 'form-select'}),
            'enfermedad_huerfana': forms.Select(choices=[(True, 'Sí'), (False, 'No')], attrs={'class': 'form-select'}),
            'enfermedad_nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'conflicto_armado': forms.Select(choices=[(True, 'Sí'), (False, 'No')], attrs={'class': 'form-select'}),
            'tipo_sangre': forms.Select(attrs={'class': 'form-select'}),
            'otro_nivel_educativo': forms.TextInput(attrs={'class': 'form-control'}),
            'pertenece_organizacion': forms.Select(choices=[(True, 'Sí'), (False, 'No')], attrs={'class': 'form-select'}),
            'nombre_organizacion': forms.TextInput(attrs={'class': 'form-control'})
        }

    def clean(self):
        cleaned_data = super().clean()
        discapacidad = cleaned_data.get("discapacidad")
        tipo_discapacidad = cleaned_data.get("tipo_discapacidad")
        if discapacidad == "Sí" and not tipo_discapacidad:
            raise ValidationError("Debe seleccionar un tipo de discapacidad si ha indicado que posee una.")
        return cleaned_data

nivel_educativo = forms.ModelMultipleChoiceField(
    queryset=NivelEducativo.objects.all(),
    widget=forms.CheckboxSelectMultiple,
    required=False,
    label="Nivel educativo alcanzado")


# ✅ Formulario para Acudiente (Fuera de DatosComplementariosForm)
class AcudienteForm(forms.ModelForm):
    class Meta:
        model = Acudiente
        exclude = ['participante']  # Se asigna manualmente desde la vista
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de contacto'}),
            'ocupacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ocupación'}),
            'parentesco': forms.Select(attrs={'class': 'form-select'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Dirección completa'}),
        }

    def clean_telefono(self):
        telefono = self.cleaned_data.get("telefono")
        if not telefono.isdigit():
            raise forms.ValidationError("El teléfono debe contener solo números.")
        return telefono



class CursoExtendidoForm(forms.ModelForm):
    class Meta:
        model = CursoExtendido
        fields = ['tipo_curso', 'disciplina', 'horario', 'lugar', 'docente']
        widgets = {
            'tipo_curso': forms.Select(attrs={'class': 'form-select'}),
            'disciplina': forms.Select(attrs={'class': 'form-select'}),
            'horario': forms.TimeInput(format='%H:%M', attrs={'type': 'time', 'class': 'form-control'}),
            'lugar': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'docente': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['disciplina'].queryset = Disciplina.objects.none()

        if 'tipo_curso' in self.data:
            tipo = self.data.get('tipo_curso')
            self.fields['disciplina'].queryset = Disciplina.objects.filter(tipo=tipo)
        elif self.instance.pk:
            self.fields['disciplina'].queryset = Disciplina.objects.filter(tipo=self.instance.tipo_curso)
        

    def clean_disciplina(self):
        disciplina = self.cleaned_data.get("disciplina")
        if not disciplina:
            raise forms.ValidationError("Debe seleccionar una disciplina.")
        return disciplina


class DocumentoRequisitoForm(forms.ModelForm):
    class Meta:
        model = DocumentoRequisito
        fields = '__all__'
        widgets = {
            'fecha_carga': forms.HiddenInput(),
        }

        

class RequisitosForm(forms.ModelForm):
    class Meta:
        model = DocumentoRequisito
        fields = [
            'formulario_inscripcion_firmado',
            'documento_identidad',
            'certificado_eps',
            'certificacion_residencia',
            'consentimiento_informado',
        ]
class DisciplinaForm(forms.ModelForm):
    class Meta:
        model = Disciplina
        fields = ['nombre', 'tipo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la disciplina'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
        }

    # 🟢 Esta parte debe ir FUERA de la clase Meta
    def clean_nombre(self):
        nombre = self.cleaned_data['nombre'].strip()
        if Disciplina.objects.filter(nombre__iexact=nombre).exists():
            raise forms.ValidationError("❌ Esta disciplina ya existe.")
        return nombre



class SeleccionarCursoForm(forms.Form):
    curso = forms.ModelChoiceField(
        queryset=CursoExtendido.objects.all(),
        label="Seleccione un curso",
        widget=forms.Select(attrs={"class": "form-select"})
    )
    
    
# forms.py

class CursoAsignacionForm(forms.Form):
    curso = forms.ModelChoiceField(
        queryset=CursoExtendido.objects.none(),  # se ajusta dinámicamente
        label="Curso Disponible",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def __init__(self, *args, **kwargs):
        tipo_area = kwargs.pop('tipo_area', None)  # 👈 extraemos tipo_area del kwargs
        super().__init__(*args, **kwargs)

        if tipo_area:
            self.fields['curso'].queryset = CursoExtendido.objects.filter(disciplina__tipo=tipo_area)
        else:
            self.fields['curso'].queryset = CursoExtendido.objects.all()




# views.py


def formulario_curso(request):
    participante_id = request.session.get("participante_id")
    participante = get_object_or_404(Participante, id=participante_id)

    tipo_area = participante.curso.tipo  # O desde sesión si ya lo definiste en pasos previos

    if request.method == "POST":
        form = CursoAsignacionForm(request.POST, tipo_area=tipo_area)
        if form.is_valid():
            curso = form.cleaned_data["curso"]
            participante.curso = curso
            participante.save()

            messages.success(request, "✅ ¡Curso asignado correctamente!")
            return redirect("resumen_registro", participante_id=participante.id)
    else:
        form = CursoAsignacionForm(tipo_area=tipo_area)

    return render(request, "formulario/formulario_curso.html", {
        "form": form,
        "participante": participante
    })
    