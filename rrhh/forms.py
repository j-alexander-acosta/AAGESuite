from django import forms
from django.db.models import Sum
from django.contrib.auth.models import User
from localflavor.cl.forms import CLRutField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, HTML
from rrhh.models.base import Funcion
from rrhh.models.persona import Persona, Funcionario, Documento
from rrhh.models.entidad import Entidad, Entrevista, Vacacion, Contrato, Licencia, Permiso
from rrhh.models.entidad import Finiquito, Solicitud, EstadoSolicitud


class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        exclude = ['usuario']

        help_texts = {
            'titulado': u"Marque si la persona tiene un título profesional",
            'religion': u"Marque si la persona pertenece a esta religión",
            'telefono': u"Si es un número móvil, la forma debe ser 9 1234 5678;\n"
                        u"en el caso de ser fijo, 45 2 711234",
        }

    rut = CLRutField()

    def __init__(self, *args, **kwargs):
        super(PersonaForm, self).__init__(*args, **kwargs)
        self.fields['fecha_nacimiento'] = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), input_formats=['%Y-%m-%d'])
        self.fields['fecha_nacimiento'].widget.attrs['class'] = 'datepicker'
        self.fields['direccion'].widget.attrs['required'] = 'required'
        self.fields['ciudad'].widget.attrs['required'] = 'required'
        self.fields['direccion'].label = 'Dirección*'
        self.fields['ciudad'].label = 'Ciudad*'
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                Div(
                    Field('rut'),
                    css_class="col-md-6"
                ),
                Div(
                    Field('fecha_nacimiento'),
                    css_class="col-md-6"
                ),
                css_class="row"
            ),
            Div(
                Div(
                    Field('nombres'),
                    css_class="col-md-4"
                ),
                Div(
                    Field('apellido_paterno'),
                    css_class="col-md-4"
                ),
                Div(
                    Field('apellido_materno'),
                    css_class="col-md-4"
                ),
                css_class="row"
            ),
            Div(
                Div(
                    Field('genero'),
                    css_class="col-md-4"
                ),
                Div(
                    Field('nacionalidad'),
                    css_class="col-md-4"
                ),
                Div(
                    Field('estado_civil'),
                    css_class="col-md-4"
                ),
                css_class="row"
            ),
            Div(
                Div(
                    Field('direccion'),
                    css_class="col-md-6"
                ),
                Div(
                    Field('ciudad'),
                    css_class="col-md-6"
                ),
                css_class="row"
            ),
            Div(
                Div(
                    Field('telefono'),
                    css_class="col-md-6"
                ),
                Div(
                    Field('email'),
                    css_class="col-md-6"
                ),
                css_class="row"
            ),
            Div(
                Div(
                    Field('titulado'),
                    css_class="col-md-6"
                ),
                Div(
                    Field('profesion'),
                    css_class="col-md-6"
                ),
                css_class="row"
            ),
            Div(
                Div(
                    Field('religion'),
                    css_class='col-md-4'
                ),
                Div(
                    Field('foto'),
                    css_class='col-md-4'
                ),
                Div(
                    Field('curriculum'),
                    css_class='col-md-4'
                ),
                css_class='row'
            )
        )

    def clean_direccion(self):
        direccion = self.cleaned_data['direccion']
        if not direccion:
            raise forms.ValidationError(
                u"Este campo es obligatorio"
            )
        return direccion

    def clean_ciudad(self):
        ciudad = self.cleaned_data['ciudad']
        if not ciudad:
            raise forms.ValidationError(
                u"Este campo es obligatorio"
            )
        return ciudad

    def clean_telefono(self):
        telefono = self.cleaned_data['telefono']
        if len(str(telefono)) != 9:
            raise forms.ValidationError(
                u"El número debe ser de nueve dígitos"
            )
        return telefono


class AsignarUsuarioPersonaForm(forms.Form):
    usuarios_utilizados = Persona.objects.filter(usuario__isnull=False).values_list('usuario__id')
    usuarios = User.objects.all().exclude(id__in=usuarios_utilizados)
    usuario = forms.ModelChoiceField(
        queryset=usuarios,
        label="Usuario"
    )

    def __init__(self, *args, **kwargs):
        super(AsignarUsuarioPersonaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(FuncionarioForm, self).__init__(*args, **kwargs)
        self.fields['persona'].widget.attrs['readonly'] = True
        self.fields['fecha_ingreso_sea'] = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), input_formats=['%Y-%m-%d'])
        self.fields['fecha_ingreso_sea'].widget.attrs['class'] = 'datepicker'
        self.fields['fecha_ingreso_docente'] = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), input_formats=['%Y-%m-%d'])
        self.fields['fecha_ingreso_docente'].widget.attrs['class'] = 'datepicker'
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'persona',
            Div(
                Div(
                    Field('afp'),
                    css_class="col-md-4"
                ),
                Div(
                    Field('salud'),
                    css_class="col-md-4"
                ),
                Div(
                    Field('isapre'),
                    css_class="col-md-4"
                ),
                css_class="row"
            ),
            Div(
                Div(
                    Field('fecha_ingreso_docente'),
                    css_class="col-md-6"
                ),
                Div(
                    Field('fecha_ingreso_sea'),
                    css_class="col-md-6"
                ),
                css_class="row"
            ),
            Div(
                Div(
                    Field('estado'),
                    css_class="col-md-4"
                ),
                Div(
                    Field('tipo_misionero'),
                    css_class="col-md-4"
                ),
                Div(
                    Field('puntos'),
                    css_class="col-md-4"
                ),
                css_class="row"
            ),
        )


class EntrevistaForm(forms.ModelForm):
    class Meta:
        model = Entrevista
        fields = ('contrato',
                  'entrevistador',
                  'tipo',
                  'contenido',
                  'acuerdos',
                  'fecha')

    def __init__(self, *args, **kwargs):
        super(EntrevistaForm, self).__init__(*args, **kwargs)
        self.fields['fecha'] = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), input_formats=['%Y-%m-%d'])
        self.fields['fecha'].widget.attrs['class'] = 'datepicker'
        self.helper = FormHelper()
        self.helper.form_tag = False


class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        exclude = (
            'fecha_carga',
        )
        widgets = {
            'perfeccionamiento': forms.HiddenInput,
            'contrato': forms.HiddenInput,
            'licencia': forms.HiddenInput,
            'permiso': forms.HiddenInput,
            'finiquito': forms.HiddenInput,
            'tipo_documento': forms.HiddenInput
        }

    def __init__(self, *args, **kwargs):
        super(DocumentoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


class AgregarDocumentoForm(forms.ModelForm):

    class Meta:
        model = Documento
        fields = '__all__'
        exclude = (
            'fecha_carga',
        )
        help_texts = {
            'documento': u'Cargue el documento firmado por ambas partes'
        }
        widgets = {
            'perfeccionamiento': forms.HiddenInput,
            'contrato': forms.HiddenInput,
            'licencia': forms.HiddenInput,
            'permiso': forms.HiddenInput,
            'finiquito': forms.HiddenInput
        }
    
    def __init__(self, *args, **kwargs):
        super(AgregarDocumentoForm, self).__init__(*args, **kwargs)
        self.fields['tipo_documento'].queryset = Documento.objects.filter(tipo_documento='otro')
        self.helper = FormHelper()
        self.helper.form_tag = False


class VacacionForm(forms.ModelForm):
    class Meta:
        model = Vacacion
        fields = [
            'contrato',
            'total_dias',
            'fecha_inicio',
            'fecha_termino',
            'total_feriados',
            'fecha_retorno',
            'es_pendiente'
        ]
        help_texts = {
            'total_feriados': u"Considerar dias que no se trabaja como dias feriados (ej. fin de semana)"
        }

    def __init__(self, *args, **kwargs):
        super(VacacionForm, self).__init__(*args, **kwargs)
        self.fields['contrato'].widget.attrs['class'] = 'chosen'
        self.fields['fecha_inicio'] = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), input_formats=['%Y-%m-%d'])
        self.fields['fecha_inicio'].widget.attrs['class'] = 'datepicker'
        self.fields['fecha_termino'] = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), input_formats=['%Y-%m-%d'])
        self.fields['fecha_termino'].widget.attrs['class'] = 'datepicker'
        self.fields['fecha_retorno'] = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), input_formats=['%Y-%m-%d'])
        self.fields['fecha_retorno'].widget.attrs['class'] = 'datepicker'
        self.helper = FormHelper()
        self.helper.form_tag = False


class VacacionTipoFuncionarioColegioForm(forms.ModelForm):
    class Meta:
        model = Vacacion
        fields = [
            'contrato',
            'total_dias',
            'fecha_inicio',
            'fecha_termino',
            'fecha_retorno',
            'total_feriados',
            'es_pendiente',
        ]
        widgets = {
            'contrato': forms.HiddenInput
        }

    def __init__(self, *args, **kwargs):
        super(VacacionTipoFuncionarioColegioForm, self).__init__(*args, **kwargs)
        self.fields['fecha_inicio'] = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), input_formats=['%Y-%m-%d'])
        self.fields['fecha_inicio'].widget.attrs['class'] = 'datepicker'
        self.fields['fecha_termino'] = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), input_formats=['%Y-%m-%d'])
        self.fields['fecha_termino'].widget.attrs['class'] = 'datepicker'
        self.fields['fecha_retorno'] = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), input_formats=['%Y-%m-%d'])
        self.fields['fecha_retorno'].widget.attrs['class'] = 'datepicker'
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'contrato',
            Div(
                Div(
                    Div(
                        Field('total_dias'),
                        css_class='col-md-6'
                    ),
                    Div(
                        Field('es_pendiente'),
                        css_class='col-md-6'
                    ),
                    css_class='row'
                ),
                Div(
                    Div(
                        Field('fecha_inicio'),
                        css_class='col-md-6'
                    ),
                    Div(
                        Field('total_feriados'),
                        css_class='col-md-6'
                    ),
                    css_class='row'
                ),
                Div(
                    Div(
                        Field('fecha_termino'),
                        css_class='col-md-6'
                    ),
                    Div(
                        Field('fecha_retorno'),
                        css_class='col-md-6'
                    ),
                    css_class='row'
                ),
            )
        )


class LicenciaForm(forms.ModelForm):
    class Meta:
        model = Licencia
        fields = [
            'contrato',
            'tipo_licencia',
            'tipo_licencia_descripcion',
            'folio_licencia',
            'total_dias',
            'fecha_inicio',
            'fecha_termino',
            'total_feriados',
            'fecha_retorno',
            'dias_habiles',
        ]

    def __init__(self, *args, **kwargs):
        super(LicenciaForm, self).__init__(*args, **kwargs)
        self.fields['contrato'].widget.attrs['class'] = 'chosen'
        self.fields['tipo_licencia'].widget.attrs['class'] = 'chosen'
        self.fields['fecha_inicio'] = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), input_formats=['%Y-%m-%d'])
        self.fields['fecha_inicio'].widget.attrs['class'] = 'datepicker'
        self.fields['fecha_termino'] = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), input_formats=['%Y-%m-%d'])
        self.fields['fecha_termino'].widget.attrs['class'] = 'datepicker'
        self.fields['fecha_retorno'] = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), input_formats=['%Y-%m-%d'])
        self.fields['fecha_retorno'].widget.attrs['class'] = 'datepicker'
        self.helper = FormHelper()
        self.helper.form_tag = False


class LicenciaTipoFuncionarioColegioForm(forms.ModelForm):
    class Meta:
        model = Licencia
        fields = [
            'contrato',
            'tipo_licencia',
            'tipo_licencia_descripcion',
            'folio_licencia',
            'total_dias',
            'fecha_inicio',
            'fecha_termino',
            'fecha_retorno',
            'total_feriados',
            'dias_habiles',
        ]
        help_texts = {
            'dias_habiles': u'Información necesaria para el cálculo de fechas'
        }
        widgets = {
            'contrato': forms.HiddenInput
        }

    def __init__(self, *args, **kwargs):
        super(LicenciaTipoFuncionarioColegioForm, self).__init__(*args, **kwargs)
        self.fields['tipo_licencia'].widget.attrs['class'] = 'chosen'
        self.fields['fecha_inicio'] = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), input_formats=['%Y-%m-%d'])
        self.fields['fecha_inicio'].widget.attrs['class'] = 'datepicker'
        self.fields['fecha_termino'] = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), input_formats=['%Y-%m-%d'])
        self.fields['fecha_termino'].widget.attrs['class'] = 'datepicker'
        self.fields['fecha_retorno'] = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), input_formats=['%Y-%m-%d'])
        self.fields['fecha_retorno'].widget.attrs['class'] = 'datepicker'
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'contrato',
            'tipo_licencia',
            'tipo_licencia_descripcion',
            Div(
                Div(
                    Div(
                        Field('folio_licencia'),
                        css_class='col-md-4'
                    ),
                    Div(
                        Field('total_dias'),
                        css_class='col-md-4'
                    ),
                    Div(
                        Field('dias_habiles'),
                        css_class='col-md-4'
                    ),
                    css_class='row'
                ),
                Div(
                    Div(
                        Field('fecha_inicio'),
                        css_class='col-md-6'
                    ),
                    Div(
                        Field('total_feriados'),
                        css_class='col-md-6'
                    ),
                    css_class='row'
                ),
                Div(
                    Div(
                        Field('fecha_termino'),
                        css_class='col-md-6'
                    ),
                    Div(
                        Field('fecha_retorno'),
                        css_class='col-md-6'
                    ),
                    css_class='row'
                ),
            )
        )


class PermisoForm(forms.ModelForm):
    documento = forms.FileField()

    class Meta:
        model = Permiso
        fields = '__all__'
        help_texts = {
            'goce_sueldo': u'Marque si corresponde',
            'documento': u'Cargue el permiso firmado por ambas partes'
        }

    def __init__(self, *args, **kwargs):
        super(PermisoForm, self).__init__(*args, **kwargs)
        self.fields['contrato'].widget.attrs['class'] = 'chosen'
        self.fields['fecha_solicitud'] = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), input_formats=['%Y-%m-%d'])
        self.fields['fecha_solicitud'].widget.attrs['class'] = 'datepicker'
        self.fields['fecha_inicio'] = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), input_formats=['%Y-%m-%d'])
        self.fields['fecha_inicio'].widget.attrs['class'] = 'datepicker'
        self.fields['fecha_termino'] = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), input_formats=['%Y-%m-%d'])
        self.fields['fecha_termino'].widget.attrs['class'] = 'datepicker'
        self.fields['fecha_retorno'] = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), input_formats=['%Y-%m-%d'])
        self.fields['fecha_retorno'].widget.attrs['class'] = 'datepicker'
        self.fields['voto'].widget.attrs['required'] = 'required'
        self.helper = FormHelper()
        self.helper.form_tag = False


class PermisoTipoFuncionarioColegioForm(forms.ModelForm):
    documento = forms.FileField()

    class Meta:
        model = Permiso
        fields = '__all__'
        help_texts = {
            'dias_habiles': u'Información necesaria para el cálculo de fechas',
            'goce_sueldo': u'Marque si corresponde'
        }
        widgets = {
            'contrato': forms.HiddenInput
        }

    def __init__(self, *args, **kwargs):
        super(PermisoTipoFuncionarioColegioForm, self).__init__(*args, **kwargs)
        self.fields['fecha_solicitud'] = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), input_formats=['%Y-%m-%d'])
        self.fields['fecha_solicitud'].widget.attrs['class'] = 'datepicker'
        self.fields['fecha_inicio'] = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), input_formats=['%Y-%m-%d'])
        self.fields['fecha_inicio'].widget.attrs['class'] = 'datepicker'
        self.fields['fecha_termino'] = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), input_formats=['%Y-%m-%d'])
        self.fields['fecha_termino'].widget.attrs['class'] = 'datepicker'
        self.fields['fecha_retorno'] = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), input_formats=['%Y-%m-%d'])
        self.fields['fecha_retorno'].widget.attrs['class'] = 'datepicker'
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'contrato',
            'observaciones',
            Div(
                Div(
                    Div(
                        Field('fecha_solicitud'),
                        css_class='col-md-4'
                    ),
                    Div(
                        Field('total_dias'),
                        css_class='col-md-4'
                    ),
                    Div(
                        Field('dias_habiles'),
                        css_class='col-md-4'
                    ),
                    css_class='row'
                ),
                Div(
                    Div(
                        Field('fecha_inicio'),
                        css_class='col-md-6'
                    ),
                    Div(
                        Field('total_feriados'),
                        css_class='col-md-6'
                    ),
                    css_class='row'
                ),
                Div(
                    Div(
                        Field('fecha_termino'),
                        css_class='col-md-6'
                    ),
                    Div(
                        Field('fecha_retorno'),
                        css_class='col-md-6'
                    ),
                    css_class='row'
                ),
                Div(
                    Div(
                        Field('voto'),
                        css_class='col-md-6'
                    ),
                    Div(
                        Field('goce_sueldo'),
                        css_class='col-md-6'
                    ),
                    css_class='row'
                ),
            ),
            'documento'
        )


class ContratoForm(forms.ModelForm):
    class Meta:
        model = Contrato
        exclude = [
            'vigente'
        ]

    def __init__(self, *args, **kwargs):
        super(ContratoForm, self).__init__(*args, **kwargs)
        self.fields['funcionario'].widget.attrs['class'] = 'chosen'
        self.fields['entidad'].queryset = Entidad.objects.filter(tipo_entidad='colegio')
        self.fields['categoria'].widget.attrs['class'] = 'chosen'
        self.fields['funcion_principal'].queryset = Funcion.objects.filter(tipo=1) 
        self.fields['funcion_secundaria'].queryset = Funcion.objects.filter(tipo=2) 
        self.fields['tipo_contrato'].widget.attrs['class'] = 'chosen'
        self.fields['reemplazando_licencia'].widget.attrs['class'] = 'chosen'
        self.fields['reemplazando_permiso'].widget.attrs['class'] = 'chosen'
        self.fields['fecha_inicio'] = forms.DateField(
            widget=forms.widgets.DateInput(attrs={'type': 'date'}),
            input_formats=['%Y-%m-%d']
        )
        self.fields['fecha_inicio'].widget.attrs['class'] = 'datepicker'
        self.fields['fecha_termino'] = forms.DateField(
            widget=forms.widgets.DateInput(attrs={'type': 'date'}),
            input_formats=['%Y-%m-%d'],
            required=False
        )
        self.fields['fecha_termino'].widget.attrs['class'] = 'datepicker'
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                Div(
                    Div(
                        HTML(
                            "<div class='checkbox float-right'>" +
                            "<a href='/rrhh/personas/nuevo'><i class='uil-plus'></i> Agregar Persona</a>" +
                            "</div>"
                        ),
                        Field('funcionario'),
                        css_class='col-md-6',
                    ),
                    Div(
                        Field('entidad'),
                        css_class='col-md-6'
                    ),
                    css_class='row'
                ),
                Div(
                    Div(
                        Field('categoria'),
                        css_class='col-md-4'
                    ),
                    Div(
                        Field('funcion_principal'),
                        css_class='col-md-4'
                    ),
                    Div(
                        Field('funcion_secundaria'),
                        css_class='col-md-4'
                    ),
                    css_class='row'
                ),
                Div(
                    Div(
                        Field('tipo_contrato'),
                        css_class='col-md-4'
                    ),
                    Div(
                        Field('fecha_inicio'),
                        css_class='col-md-4'
                    ),
                    Div(
                        Field('fecha_termino'),
                        css_class='col-md-4'
                    ),
                    css_class='row'
                ),
                Div(
                    Div(
                        Field('sueldo'),
                        css_class='col-md-4'
                    ),
                    Div(
                        Field('asignacion_funcion'),
                        css_class='col-md-4'
                    ),
                    Div(
                        Field('asignacion_locomocion'),
                        css_class='col-md-4'
                    ),
                    css_class='row'
                ),
                Div(
                    Div(
                        Field('horas_total'),
                        css_class='col-md-6'
                    ),
                    Div(
                        Field('reemplazando_licencia'),
                        css_class='col-md-6'
                    ),
                    css_class='row'
                ),
            )
        )

    def clean(self):
        cleaned_data = super(ContratoForm, self).clean()
        horas_total = self.cleaned_data.get('horas_total', 0)
        tipo_contrato = self.cleaned_data.get('tipo_contrato', 0)
        categoria = self.cleaned_data.get('categoria', 0)
        entidad = self.cleaned_data.get('entidad', None)
        funcionario = self.cleaned_data.get('funcionario', None)
        entidades = Entidad.objects.filter(dependiente=entidad.dependiente)
        contratos_funcionario = Contrato.objects.filter(
            funcionario=funcionario,
            entidad__in=entidades,
            vigente=True,
            reemplazando_permiso=None,
            reemplazando_licencia=None
        )
        cfh = contratos_funcionario.values('funcionario').annotate(
            horas=Sum('horas_total')
        )

        if contratos_funcionario.exists():
            horas_total += cfh[0]['horas']

        horas_esperadas = 45
        if categoria == 2:
            horas_esperadas = 44

        if horas_total > horas_esperadas:
            msg = "Las horas contratadas para este Funcionario, supera el límite de {} horas, por {} horas".format(horas_esperadas, horas_total - horas_esperadas)
            self.add_error('horas_total', msg)

        if tipo_contrato == 2:
            cfc = contratos_funcionario.values_list('tipo_contrato')
            if cfc.count() >= 3:
                cfc = list(cfc)[-3:]
            cpf = 0
            for tp in cfc:
                if tp[0] == 2:
                    cpf += 1
            if cpf >= 3:
                msg = "Ya existen 3 contratos a plazo fijo"
                self.add_error('tipo_contrato', msg)

        return cleaned_data


class FiniquitoForm(forms.ModelForm):
    documento = forms.FileField()

    class Meta:
        model = Finiquito
        fields = [
            'contrato',
            'razon_baja',
            'descripcion',
        ]

        widgets = {
            'contrato': forms.HiddenInput
        }

    def __init__(self, *args, **kwargs):
        super(FiniquitoForm, self).__init__(*args, **kwargs)
        self.fields['razon_baja'].widget.attrs['class'] = 'chosen'
        self.helper = FormHelper()
        self.helper.form_tag = False


class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        exclude = [
            'postulantes'
        ]

        widgets = {
            'tipo': forms.HiddenInput,
            'contrato': forms.HiddenInput
        }

    def __init__(self, *args, **kwargs):
        super(SolicitudForm, self).__init__(*args, **kwargs)
        self.fields['fecha_inicio'] = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), input_formats=['%Y-%m-%d'])
        self.fields['fecha_inicio'].widget.attrs['class'] = 'datepicker'
        self.fields['fecha_termino'] = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), input_formats=['%Y-%m-%d'], required=False)
        self.fields['fecha_termino'].widget.attrs['class'] = 'datepicker'
        self.fields['entidad'].widget.attrs['class'] = 'chosen'
        self.fields['categoria'].widget.attrs['class'] = 'chosen'
        self.fields['tipo_contrato'].widget.attrs['class'] = 'chosen'
        self.fields['reemplazando_licencia'].widget.attrs['class'] = 'chosen'
        self.fields['reemplazando_permiso'].widget.attrs['class'] = 'chosen'
        self.fields['contrato'].queryset = Contrato.objects.filter(vigente=True)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'tipo',
            'contrato',
            'entidad',
            Div(
                Div(
                    Div(
                        Field('categoria'),
                        css_class='col-md-4'
                    ),
                    Div(
                        Field('cargo'),
                        css_class='col-md-4'
                    ),
                    Div(
                        Field('tipo_contrato'),
                        css_class='col-md-4'
                    ),
                    css_class='row'
                ),
                Div(
                    Div(
                        Field('horas'),
                        css_class='col-md-4'
                    ),
                    Div(
                        Field('fecha_inicio'),
                        css_class='col-md-4'
                    ),
                    Div(
                        Field('fecha_termino'),
                        css_class='col-md-4'
                    ),
                    css_class='row'
                ),
                Div(
                    Div(
                        Field('sueldo'),
                        css_class='col-md-4'
                    ),
                    Div(
                        Field('asignacion_funcion'),
                        css_class='col-md-4'
                    ),
                    Div(
                        Field('asignacion_locomocion'),
                        css_class='col-md-4'
                    ),
                    css_class='row'
                )
            ),
            'reemplazando_licencia',
            'justificacion'
        )


class EstadoSolicitudForm(forms.ModelForm):
    class Meta:
        model = EstadoSolicitud
        fields = [
            'estado',
            'observaciones',
            'voto',
        ]

        widgets = {
            'estado': forms.HiddenInput
        }

    def __init__(self, *args, **kwargs):
        super(EstadoSolicitudForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'estado',
            'observaciones',
            'voto'
        )


class EstadoContratacionForm(forms.Form):
    observaciones = forms.CharField(
        required=False,
        widget=forms.Textarea({'rows': 6})
    )
    documento = forms.FileField(
        required=False
    )
    estado = forms.IntegerField(
        required=True,
        widget=forms.HiddenInput()
    )

    def __init__(self, *args, **kwargs):
        super(EstadoContratacionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'estado',
            'observaciones',
            'documento'
        )
