from django import forms
from django.core.exceptions import ValidationError
from .models import Participante, Curso, Docente, DatosComplementarios, Acudiente, CursoExtendido, DocumentoRequisito
from datetime import date
from .choices import TIPO_AREA_CHOICES, DISCIPLINAS_CULTURA, DISCIPLINAS_DEPORTE

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


    tipo_documento = forms.ChoiceField(
        choices=TIPO_DOCUMENTO_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,
        label="Tipo de Documento"
    )

    fecha_expedicion = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=True,
        label="Fecha de Expedición"
    )

    lugar_expedicion = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lugar de expedición'}),
        required=False,
        label="Lugar de Expedición"
    )

    pais_origen = forms.ChoiceField(
        choices=PAIS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,
        label="País de Origen"
    )

    ciudad = forms.CharField(
        initial="Bogotá",
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        required=True,
        label="Ciudad"
    )

    area = forms.ChoiceField(
    choices=ZONA_GEOGRAFICA_CHOICES,
    widget=forms.Select(attrs={'class': 'form-control'}),
    required=True,
    label="Área"
)


    localidad = forms.CharField(
        initial="Kennedy",
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        required=True,
        label="Localidad"
    )

    barrio = forms.ChoiceField(
        choices=BARRIO_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,
        label="Barrio"
    )

    edad = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        label="Edad"
    )

   

    class Meta:
        model = Participante
        fields = [
            'nombre', 'tipo_documento', 'identificacion', 'fecha_expedicion', 'lugar_expedicion',
            'pais_origen', 'ciudad', 'area', 'localidad', 'barrio', 'edad', 'correo', 'telefono',
            'direccion', 'fecha_nacimiento'
        ]

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo'}),
            'identificacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de identificación'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de contacto'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección'}),
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def clean_fecha_nacimiento(self):
        """ 🔹 Calcula la edad a partir de la fecha de nacimiento """
        fecha_nacimiento = self.cleaned_data.get('fecha_nacimiento')
        if fecha_nacimiento:
            hoy = date.today()
            edad_calculada = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
            if edad_calculada < 0:
                raise ValidationError("La fecha de nacimiento no puede ser futura.")
            return fecha_nacimiento
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
    
    cursos = forms.ModelMultipleChoiceField(
        queryset=Curso.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
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
            'fecha_nacimiento', 'area_encargada', 'cursos'
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


NIVEL_EDUCATIVO_CHOICES = [
    ('Básica Primaria', 'Básica Primaria'),
    ('Básica Secundaria', 'Básica Secundaria'),
    ('Técnico', 'Técnico'),
    ('Tecnólogo', 'Tecnólogo'),
    ('Universitaria Incompleta', 'Universitaria Incompleta'),
    ('Universitaria Completa', 'Universitaria Completa'),
    ('Posgrado Incompleto', 'Posgrado Incompleto'),
    ('Posgrado Completo', 'Posgrado Completo'),
    ('Maestría', 'Maestría'),
    ('Ninguno', 'Ninguno'),
    ('Otro', 'Otro'),
]
class DatosComplementariosForm(forms.ModelForm):
    discapacidad = forms.ChoiceField(
        choices=[('No', 'No'), ('Sí', 'Sí')],
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_discapacidad'}),
        label="¿Posee alguna discapacidad?"
    )

    tipo_discapacidad = forms.ChoiceField(
        choices=[('Auditiva', 'Auditiva'),
                 ('Física', 'Física'),
                 ('Intelectual', 'Intelectual'),
                 ('Visual', 'Visual'),
                 ('Sordo-Ceguera', 'Sordo-Ceguera'),
                 ('Psicosocial', 'Psicosocial'),
                 ('Múltiple', 'Múltiple')],
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_tipo_discapacidad'}),
        required=False,
        label="Tipo de discapacidad"
    )

    nivel_educativo = forms.MultipleChoiceField(
        choices=NIVEL_EDUCATIVO_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False,
        label="Seleccione su nivel académico"
    )

    class Meta:
        model = DatosComplementarios  # Se asegura de que este formulario esté vinculado con el modelo
        fields = [
            'identidad_genero', 'grupo_etnico', 'discapacidad', 'tipo_discapacidad',
            'enfermedad_huerfana', 'enfermedad_nombre', 'conflicto_armado',
            'tipo_sangre', 'nivel_educativo', 'otro_nivel_educativo',
            'pertenece_organizacion', 'nombre_organizacion'
        ]
        widgets = {
            'identidad_genero': forms.Select(attrs={'class': 'form-select'}),
            'grupo_etnico': forms.Select(attrs={'class': 'form-select'}),
            'enfermedad_huerfana': forms.Select(choices=[(True, 'Sí'), (False, 'No')], attrs={'class': 'form-select', 'id': 'id_enfermedad_huerfana'}),
            'enfermedad_nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Especificar enfermedad', 'id': 'id_enfermedad_nombre'}),
            'conflicto_armado': forms.Select(choices=[(True, 'Sí'), (False, 'No')], attrs={'class': 'form-select'}),
            'tipo_sangre': forms.Select(attrs={'class': 'form-select'}),
            'nivel_educativo': forms.Select(attrs={'class': 'form-select'}),
            'otro_nivel_educativo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Especificar si eligió "Otro"'}),
            'pertenece_organizacion': forms.Select(choices=[(True, 'Sí'), (False, 'No')], attrs={'class': 'form-select'}),
            'nombre_organizacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la organización'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        discapacidad = cleaned_data.get("discapacidad")
        tipo_discapacidad = cleaned_data.get("tipo_discapacidad")

        if discapacidad == "Sí" and not tipo_discapacidad:
            raise ValidationError("Debe seleccionar un tipo de discapacidad si ha indicado que posee una.")

        return cleaned_data

    
    
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
        fields = ['tipo_curso', 'disciplina']
        widgets = {
            'tipo_curso': forms.Select(attrs={'class': 'form-control'}),
            'disciplina': forms.Select(attrs={'class': 'form-control'}),
        }

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
