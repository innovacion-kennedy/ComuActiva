# formulario/choices.py
TIPO_AREA_CHOICES = [
    ('Deporte', 'Deporte'),
    ('Cultura', 'Cultura'),
]

DISCIPLINAS_DEPORTE = [
    ('Fútbol', 'Fútbol'),
    ('Basketball', 'Basketball'),
    ('Voleibol', 'Voleibol'),
]

DISCIPLINAS_CULTURA = [
    ('Danza', 'Danza'),
    ('Fotografía', 'Fotografía'),
    ('Pintura', 'Pintura'),
]

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

DISCAPACIDAD_BOOLEAN_CHOICES = [
    ('No', 'No'),
    ('Sí', 'Sí'),
]

TIPOS_DISCAPACIDAD = [
    ('Auditiva', 'Auditiva'),
    ('Física', 'Física'),
    ('Intelectual', 'Intelectual'),
    ('Visual', 'Visual'),
    ('Sordo-Ceguera', 'Sordo-Ceguera'),
    ('Psicosocial', 'Psicosocial'),
    ('Múltiple', 'Múltiple'),
]



EDUCACION_CHOICES = [
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

GENERO_CHOICES = [
    ('Masculino', 'Masculino'),
    ('Femenino', 'Femenino'),
    ('Transgénero', 'Transgénero'),
    ('Intersexual', 'Intersexual'),
    ('Otro', 'Otro'),
    ('No Responde', 'No Responde'),
]

ETNIA_CHOICES = [
    ('Indígena', 'Indígena'),
    ('Afro', 'Afro'),
    ('Comunidad Negra', 'Comunidad Negra'),
    ('Palenquero', 'Palenquero'),
    ('Raizal', 'Raizal'),
    ('Rom o Gitano', 'Rom o Gitano'),
    ('Ninguno', 'Ninguno'),
]

SANGRE_CHOICES = [
    ('A+', 'A+'), ('A-', 'A-'),
    ('B+', 'B+'), ('B-', 'B-'),
    ('AB+', 'AB+'), ('AB-', 'AB-'),
    ('O+', 'O+'), ('O-', 'O-'),
]

