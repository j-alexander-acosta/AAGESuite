from django.http import FileResponse, HttpResponse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin   
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from jsonview.decorators import json_view
from django.template.defaultfilters import yesno
from django.contrib.humanize.templatetags.humanize import naturalday
from rrhh.templatetags.rrhh_utils import *
from rrhh.models.base import TipoLicencia, DOCUMENTO, Documento
from rrhh.models.persona import Persona, Funcionario
from rrhh.models.entidad import Entrevista, Vacacion, Finiquito, Licencia, Permiso, Contrato, EstadoContratacion
from rrhh.models.entidad import Solicitud, EstadoSolicitud
from rrhh.forms import VacacionTipoFuncionarioColegioForm, VacacionForm, ContratoForm, FuncionarioForm, EntrevistaForm, AsignarUsuarioPersonaForm
from rrhh.forms import PermisoTipoFuncionarioColegioForm, PermisoForm, SolicitudForm, EstadoSolicitudForm, DocumentoForm, AgregarDocumentoForm
from rrhh.forms import LicenciaTipoFuncionarioColegioForm, LicenciaForm, PersonaForm, FiniquitoForm, EstadoContratacionForm
from rrhh.pdf.descuentodiezmo import DescuentoDiezmo
from rrhh.pdf.detallecontrato import DetalleContrato
from rrhh.pdf.autorizacionimagen import AutorizacionImagen
from rrhh.pdf.conocimientoreglameto import TomaConocimientoReglamentoInterno

@login_required
def home(request):
    # Contratos
    contratos = Contrato.objects.all()
    contratos_expirar = []
    contratos_finiquitar = []
    contratos_contratar = []
    for c in contratos:
        if c.vigente:
            if c.categoria == 2 and c.dias_termino_contrato <= 120:
                if c.solicitud_set.all():
                    contratos_finiquitar.append(c)
                else:
                    contratos_expirar.append(c)
            elif c.dias_termino_contrato <= 60:
                if c.solicitud_set.all():
                    contratos_finiquitar.append(c)
                else:
                    contratos_expirar.append(c)
        elif c.estado_id != 4:
            contratos_contratar.append(c)

    # Solicitudes
    solicitudes = Solicitud.objects.filter()
    solicitudes_pendientes = []
    estados_pendientes = [2, 4, 5, 6]
    for s in solicitudes:
        if s.estado_id in estados_pendientes:
            solicitudes_pendientes.append(s)

    context = {
        'contratos_contratar': contratos_contratar,
        'contratos_expirar': contratos_expirar,
        'contratos_finiquitar': contratos_finiquitar,
        'solicitudes_pendientes': solicitudes_pendientes,
    }

    return render(request, 'rrhh/home.html', context)


@login_required
def hyper_index(request):
    return render(request, 'rrhh/hyper_index.html')


class PersonaListView(LoginRequiredMixin, ListView):
    """
        Listado de periodos
    """
    model = Persona
    template_name = 'rrhh/persona/listado_persona.html'
    #TODO agregar paginacion


class PersonaCreateView(LoginRequiredMixin, CreateView):
    model = Persona
    form_class = PersonaForm
    template_name = 'rrhh/persona/nuevo_persona.html'

    def get_success_url(self):
        if self.request.POST.get('funcionario'):
            return reverse_lazy('rrhh:funcionario__nuevo', args=[str(self.object.id)])
        else:
            return reverse_lazy('rrhh:persona', args=[str(self.object.id)])


@login_required
def persona_detail(request, pk_persona):
    context = {}
    persona = get_object_or_404(
        Persona,
        pk=pk_persona
    )

    context['object'] = persona
    context['asignar_up_form'] = AsignarUsuarioPersonaForm()

    if request.method == 'POST':
        form = AsignarUsuarioPersonaForm(request.POST)
        if form.is_valid():
            usuario = form.cleaned_data.get('usuario')
            persona.usuario = usuario
            persona.save()
            messages.add_message(request, messages.SUCCESS, 'Usuario asignado satisfactoriamente')
        else:
            context['asignar_up_form'] = form
            messages.add_message(request, messages.WARNING, 'Porfavor, complete la información requerida')

    return render(
        request,
        'rrhh/persona/perfil2.html',
        context
    )


class PersonaDetailView(LoginRequiredMixin, DetailView):
    model = Persona
    template_name = 'rrhh/persona/perfil.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lf_form'] = LicenciaTipoFuncionarioColegioForm(instance=self)
        return context


class PersonaUpdateView(LoginRequiredMixin, UpdateView):
    model = Persona
    form_class = PersonaForm
    template_name = 'rrhh/persona/editar_persona.html'

    def get_success_url(self):
        return reverse_lazy(
            'rrhh:persona',
            kwargs={
                'pk_persona': self.object.pk,
            }
        )


class PersonaDeleteView(LoginRequiredMixin, DeleteView):
    model = Persona
    success_url = reverse_lazy('rrhh:personas')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


# class FuncionarioListView(LoginRequiredMixin, ListView):
#     model = Funcionario
#     template_name = 'rrhh/funcionario/listado_funcionario.html'
#     paginate_by = 10
#
#
class FuncionarioCreateView(LoginRequiredMixin, CreateView):
    model = Funcionario
    form_class = FuncionarioForm
    template_name = 'rrhh/funcionario/nuevo_funcionario.html'

    def get_success_url(self):
        return reverse_lazy(
            'rrhh:persona',
            kwargs={
                'pk': self.object.persona.pk,
            }
        )


@login_required
def crear_funcionario(request, id_persona):
    persona = get_object_or_404(
        Persona,
        id=id_persona
    )
    context = {}

    if request.method == 'POST':
        form = FuncionarioForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('rrhh:persona', persona.id)
        else:
            # Formulario con errores
            messages.add_message(request, messages.WARNING, 'Porfavor, complete la información requerida')
            context['message'] = u"Complete la información requerida"
            context['form'] = form

    else:
        form = FuncionarioForm(
            initial={
                'persona': persona
            },
        )
        context['form'] = form

    return render(
        request,
        'rrhh/funcionario/nuevo_funcionario.html',
        context
    )


# class FuncionarioDetailView(LoginRequiredMixin, DetailView):
#     model = Funcionario
#     template_name = 'rrhh/funcionario/detalle_funcionario.html'
#
#


class FuncionarioUpdateView(LoginRequiredMixin, UpdateView):
    model = Funcionario
    form_class = FuncionarioForm
    template_name = 'rrhh/funcionario/nuevo_funcionario.html'

    def get_success_url(self):
        return reverse_lazy('rrhh:persona', args=[str(self.object.persona.id)])


#
# class FuncionarioDeleteView(LoginRequiredMixin, DeleteView):
#     model = Funcionario
#     success_url = reverse_lazy('rrhh:funcionarios')
#
#     def get(self, request, *args, **kwargs):
#        return self.post(request, *args, **kwargs)


@login_required
def postulantes(request):
    context = {}
    postulantes = {p for p in Persona.objects.all() if 'Postulante' in p.clasificacion}

    context['postulantes'] = postulantes

    return render(
        request,
        'rrhh/solicitud/postulantes.html',
        context
    )


class EntrevistaListView(LoginRequiredMixin, ListView):
    """
        Listado de periodos
    """
    model = Entrevista
    template_name = 'rrhh/entrevista/listado_entrevista.html'
    paginate_by = 10


class EntrevistaCreateView(LoginRequiredMixin, CreateView):
    model = Entrevista
    form_class = EntrevistaForm
    template_name = 'rrhh/entrevista/nueva_entrevista.html'
    success_url = reverse_lazy('rrhh:entrevistas')


class EntrevistaDetailView(LoginRequiredMixin, DetailView):
    model = Entrevista
    template_name = 'rrhh/entrevista/detalle_entrevista.html'


class EntrevistaUpdateView(LoginRequiredMixin, UpdateView):
    model = Entrevista
    form_class = EntrevistaForm
    template_name = 'rrhh/entrevista/editar_entrevista.html'

    def get_success_url(self):
        return reverse_lazy(
            'rrhh:entrevista',
            kwargs={
                'pk': self.object.pk,
            }
        )


class EntrevistaDeleteView(LoginRequiredMixin, DeleteView):
    model = Entrevista
    success_url = reverse_lazy('rrhh:entrevistas')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class DocumentoListView(LoginRequiredMixin, ListView):
    model = Documento
    template_name = 'rrhh/documento/listado_documento.html'
    paginate_by = 10


class DocumentoCreateView(LoginRequiredMixin, CreateView):
    model = Documento
    form_class = DocumentoForm
    template_name = 'rrhh/documento/nuevo_documento.html'
    success_url = reverse_lazy('rrhh:documentos')


class DocumentoDetailView(LoginRequiredMixin, DetailView):
    model = Documento
    template_name = 'rrhh/documento/detalle_documento.html'


class DocumentoUpdateView(LoginRequiredMixin, UpdateView):
    model = Documento
    form_class = DocumentoForm
    template_name = 'rrhh/documento/editar_documento.html'

    def get_success_url(self):
        return reverse_lazy(
            'rrhh:documento',
            kwargs={
                'pk': self.object.pk,
            }
        )


class DocumentoDeleteView(LoginRequiredMixin, DeleteView):
    model = Documento
    success_url = reverse_lazy('rrhh:documentos')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class VacacionListView(LoginRequiredMixin, ListView):
    model = Vacacion
    template_name = 'rrhh/vacacion/listado_vacacion.html'
    search_fields = ['contrato__persona__rut', 'contrato__persona']
    paginate_by = 10


class VacacionDetailView(LoginRequiredMixin, DetailView):
    model = Vacacion
    template_name = 'rrhh/vacacion/detalle_vacacion.html'


class VacacionCreateView(LoginRequiredMixin, CreateView):
    model = Vacacion
    form_class = VacacionForm
    template_name = 'rrhh/vacacion/nueva_vacacion.html'
    success_url = reverse_lazy('rrhh:vacaciones')


class VacacionUpdateView(LoginRequiredMixin, UpdateView):
    model = Vacacion
    form_class = VacacionForm
    template_name = 'rrhh/vacacion/editar_vacacion.html'

    def get_success_url(self):
        return reverse_lazy(
            'rrhh:vacacion',
            kwargs={
                'pk': self.object.pk,
            }
        )


class VacacionDeleteView(LoginRequiredMixin, DeleteView):
    model = Vacacion
    success_url = reverse_lazy('rrhh:vacaciones')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


@login_required
@json_view
def nuevo_vacacion_funcionario(request):
    """
        Función para crear un nuevo registro de vacacion a un funcionario

    :param request: Django Request
    :return: Json
    """
    data = {
        'success': False,
        'message': u"",
        'form_html': None
    }

    if request.method == 'GET':
        contrato = get_object_or_404(
            Contrato,
            id=request.GET.get('contrato', None)
        )
        total_dias = request.GET.get('total_dias', None)
        fecha_inicio = request.GET.get('fecha_inicio', None)
        fecha_termino = request.GET.get('fecha_termino', None)
        fecha_retorno = request.GET.get('fecha_retorno', None)
        total_feriados = request.GET.get('total_feriados', None)
        # dias_pendiente = request.GET.get('dias_pendiente', None)
        es_pendiente = request.GET.get('es_pendiente', None)

        vacacion = Vacacion.objects.create(
            contrato=contrato,
            total_dias=total_dias,
            fecha_inicio=fecha_inicio,
            fecha_termino=fecha_termino,
            fecha_retorno=fecha_retorno,
            total_feriados=total_feriados,
            # dias_pendiente=dias_pendiente,
            es_pendiente=es_pendiente
        )
        data['success'] = True
        data['message'] = u"la licencia fue agregada exitosamente"
        data['periodo'] = vacacion.periodo
        data['total_dias'] = vacacion.total_dias
        # data['dias_pendiente'] = vacacion.dias_pendiente
        data['fecha_retorno'] = naturalday(vacacion.fecha_retorno)
        data['total_feriados'] = vacacion.total_feriados
        data['es_pendiente'] = yesno(not vacacion.es_pendiente)
    else:
        data['message'] = u"La solicitud debe ser GET"

    return data


class LicenciaListView(LoginRequiredMixin, ListView):
    model = Licencia
    template_name = 'rrhh/licencia/listado_licencia.html'
    search_fields = ['contrato__persona', 'contrato__persona_rut']
    paginate_by = 10
    order_by = '-id'


class LicenciaDetailView(LoginRequiredMixin, DetailView):
    model = Licencia
    template_name = 'rrhh/licencia/detalle_licencia.html'


class LicenciaCreateView(LoginRequiredMixin, CreateView):
    model = Licencia
    form_class = LicenciaForm
    template_name = 'rrhh/licencia/nuevo_licencia.html'
    success_url = reverse_lazy('rrhh:licencias')


class LicenciaUpdateView(LoginRequiredMixin, UpdateView):
    model = Licencia
    form_class = LicenciaForm
    template_name = 'rrhh/licencia/nuevo_licencia.html'

    def get_success_url(self):
        return reverse_lazy(
            'rrhh:licencia',
            kwargs={
                'pk': self.object.pk,
            }
        )


class LicenciaDeleteView(LoginRequiredMixin, DeleteView):
    model = Licencia
    success_url = reverse_lazy('rrhh:licencias')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


@login_required
@json_view
def nuevo_licencia_tipo_funcionario(request):
    """
        Función para crear un nuevo registro de licencia a un uncionario

    :param request: Django Request
    :return: Json
    """
    data = {
        'success': False,
        'message': u"",
        'form_html': None
    }

    if request.method == 'GET':

        contrato = get_object_or_404(
            Contrato,
            id=request.GET.get('contrato', None)
        )
        tipo_licencia_id = request.GET.get('tipo_licencia', None)
        descripcion = request.GET.get('descripcion', None)
        folio_licencia = request.GET.get('folio_licencia', None)
        total_dias = request.GET.get('total_dias', None)
        fecha_inicio = request.GET.get('fecha_inicio', None)
        fecha_termino = request.GET.get('fecha_termino', None)
        fecha_retorno = request.GET.get('fecha_retorno', None)
        total_feriados = request.GET.get('total_feriados', None)
        dias_habiles = request.GET.get('dias_habiles', None)

        tipo_licencia = get_object_or_404(
            TipoLicencia,
            id=tipo_licencia_id
        ) if tipo_licencia_id else None

        licencia = Licencia.objects.create(
            contrato=contrato,
            tipo_licencia=tipo_licencia,
            tipo_licencia_descripcion=descripcion,
            folio_licencia=folio_licencia,
            total_dias=total_dias,
            fecha_inicio=fecha_inicio,
            fecha_termino=fecha_termino,
            fecha_retorno=fecha_retorno,
            total_feriados=total_feriados,
            dias_habiles=dias_habiles
        )

        data['success'] = True
        data['message'] = u"la licencia fue agregada exitosamente"
        data[
            'tipo_licencia'] = licencia.tipo_licencia.nombre if licencia.tipo_licencia else licencia.tipo_licencia_descripcion
        data['folio'] = beauty_none(licencia.folio_licencia)
        data['periodo'] = '{} - {}'.format(
            naturalday(licencia.fecha_inicio),
            naturalday(licencia.fecha_termino)
        )
        data['total_dias'] = licencia.total_dias
        data['fecha_retorno'] = naturalday(licencia.fecha_retorno)
        data['total_feriados'] = licencia.total_feriados
        data['dias_habiles'] = yesno(licencia.dias_habiles)

    else:
        data['message'] = u"La solicitud debe ser GET"

    return data


class PermisoListView(LoginRequiredMixin, ListView):
    model = Permiso
    template_name = 'rrhh/permiso/listado_permiso.html'
    search_fields = ['contrato__persona', 'contrato__persona_rut']
    paginate_by = 10
    order_by = '-id'


class PermisoDetailView(LoginRequiredMixin, DetailView):
    model = Permiso
    template_name = 'rrhh/permiso/detalle_permiso.html'


class PermisoCreateView(LoginRequiredMixin, CreateView):
    model = Permiso
    form_class = PermisoForm
    template_name = 'rrhh/permiso/nuevo_permiso.html'
    success_url = reverse_lazy('rrhh:permisos')


class PermisoUpdateView(LoginRequiredMixin, UpdateView):
    model = Permiso
    form_class = PermisoForm
    template_name = 'rrhh/permiso/editar_permiso.html'

    def get_success_url(self):
        return reverse_lazy(
            'rrhh:permiso',
            kwargs={
                'pk': self.object.pk,
            }
        )


class PermisoDeleteView(LoginRequiredMixin, DeleteView):
    model = Permiso
    success_url = reverse_lazy('rrhh:permisos')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


@login_required
@json_view
def nuevo_permiso_tipo_funcionario(request):
    """
        Función para crear un nuevo registro de permiso a un uncionario

    :param request: Django Request
    :return: Json
    """
    data = {
        'success': False,
        'message': u"",
        'form_html': None
    }

    if request.method == 'GET':

        contrato = get_object_or_404(
            Contrato,
            id=request.GET.get('contrato', None)
        )

        total_dias = request.GET.get('total_dias', None)
        observaciones = request.GET.get('observaciones', None)
        fecha_solicitud = request.GET.get('fecha_solicitud', None)
        fecha_inicio = request.GET.get('fecha_inicio', None)
        fecha_termino = request.GET.get('fecha_termino', None)
        fecha_retorno = request.GET.get('fecha_retorno', None)
        total_feriados = request.GET.get('total_feriados', None)
        goce_sueldo = request.GET.get('goce_sueldo', None)
        dias_habiles = request.GET.get('dias_habiles', None)
        voto = request.GET.get('voto', None)
        documento = request.GET.get('documento', None)

        permiso = Permiso.objects.create(
            contrato=contrato,
            total_dias=total_dias,
            observaciones=observaciones,
            fecha_solicitud=fecha_solicitud,
            fecha_inicio=fecha_inicio,
            fecha_termino=fecha_termino,
            fecha_retorno=fecha_retorno,
            total_feriados=total_feriados,
            goce_sueldo=goce_sueldo,
            dias_habiles=dias_habiles,
            voto=voto if voto else 0,
        )
        Documento.objects.create(
            permiso=permiso,
            tipo_documento='permiso',
            documento=documento
        )

        data['success'] = True
        data['message'] = u"El permiso fue agregada exitosamente"
        data['observaciones'] = beauty_none(permiso.observaciones)
        data['periodo'] = permiso.periodo
        data['total_dias'] = permiso.total_dias
        data['fecha_retorno'] = naturalday(permiso.fecha_retorno)
        data['total_feriados'] = permiso.total_feriados
        data['dias_habiles'] = yesno(permiso.dias_habiles)
        data['goce_sueldo'] = yesno(not permiso.goce_sueldo)
    else:
        data['message'] = u"La solicitud debe ser GET"

    return data

@login_required
@json_view
def nuevo_documento_funcionario(request):
    """
        Función para crear un nuevo registro de documento a un uncionario

    :param request: Django Request
    :return: Json
    """
    data = {
        'success': False,
        'message': u"",
        'form_html': None
    }

    if request.method == 'GET':

        contrato = get_object_or_404(
            Contrato,
            id=request.GET.get('contrato', None)
        )

        tipo_documento = request.GET.get('tipo_documento', None)
        documento = request.GET.get('documento', None)

        documento = Documento.objects.create(
            contrato=contrato,
            tipo_documento=tipo_documento,
            documento=documento
        )

        data['success'] = True
        data['message'] = u"El permiso fue agregada exitosamente"
 
        data['periodo'] = documento.periodo
        data['tipo_documento'] = documento.tipo_documento
    else:
        data['message'] = u"La solicitud debe ser GET"

    return data

@login_required
def detalle_contrato_pdf(request, pk):
    contrato = get_object_or_404(Contrato,pk=pk)
    pdf = DetalleContrato.contrato(contrato)
    return FileResponse(open('DetalleContato.pdf', 'rb'), content_type='application/pdf')   

@login_required
def Toma_conocimiento_reglamento_interno_pdf(request, pk):
    contrato = get_object_or_404(Contrato,pk=pk)
    pdf = TomaConocimientoReglamentoInterno.reglamento(contrato)
    return FileResponse(open('ConocimientoReglamentoInterno.pdf', 'rb'), content_type='application/pdf')  

@login_required
def detalle_trabajador_diezmo_pdf(request, pk):
    contrato = get_object_or_404(Contrato,pk=pk)
    pdf = DescuentoDiezmo.diezmo(contrato)
    return FileResponse(open('DescuentoDiezmo.pdf', 'rb'), content_type='application/pdf')

@login_required
def autorizacion_imagen_pdf(request, pk):
    contrato = get_object_or_404(Contrato,pk=pk)
    pdf = AutorizacionImagen.imagen(contrato)
    return FileResponse(open('Autorizacionimagen.pdf', 'rb'), content_type='application/pdf')

class ContratoListView(LoginRequiredMixin, ListView):
    model = Contrato
    template_name = 'rrhh/contrato/listado_contrato.html'
    search_fields = ['persona__rut', 'persona']
    paginate_by = 10
    ordering = ['-vigente', 'funcionario']


class ContratoDetailView(LoginRequiredMixin, DetailView):
    model = Contrato
    template_name = 'rrhh/contrato/detalle_contrato.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['documentos'] = DOCUMENTO[:4]
        context['doc_form'] = DocumentoForm(initial={'contrato': self.object.id})
        context['ec_form'] = EstadoContratacionForm(initial={'contrato': self.object.id})
        context['df_form'] = AgregarDocumentoForm(initial={'contrato': self.object.id})
        context['pf_form'] = PermisoTipoFuncionarioColegioForm(initial={'contrato': self.object.id})
        context['lf_form'] = LicenciaTipoFuncionarioColegioForm(initial={'contrato': self.object.id})
        context['vf_form'] = VacacionTipoFuncionarioColegioForm(initial={'contrato': self.object.id})
        return context


class ContratoCreateView(LoginRequiredMixin, CreateView):
    model = Contrato
    form_class = ContratoForm
    template_name = 'rrhh/contrato/nuevo_contrato.html'

    # success_url = reverse_lazy('rrhh:contratos')

    def get_success_url(self):
        EstadoContratacion.objects.create(
            contrato=self.object,
            estado=1,
            observaciones='Se inicia el proceso de contratación',
            autor=self.request.user
        )
        return reverse_lazy(
            'rrhh:contrato',
            kwargs={
                'pk': self.object.pk,
            }
        )


class ContratoUpdateView(LoginRequiredMixin, UpdateView):
    model = Contrato
    form_class = ContratoForm
    template_name = 'rrhh/contrato/editar_contrato.html'

    def get_success_url(self):
        EstadoContratacion.objects.create(
            contrato=self.object,
            estado=1,
            observaciones='Se vuelve el proceso a inicio, por actualización de los datos',
            autor=self.request.user
        )
        return reverse_lazy(
            'rrhh:contrato',
            kwargs={
                'pk': self.object.pk,
            }
        )


class ContratoDeleteView(LoginRequiredMixin, DeleteView):
    model = Contrato
    success_url = reverse_lazy('rrhh:contratos')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


@login_required
def nuevo_finiquito(request, id_contrato):
    contrato = get_object_or_404(
        Contrato,
        pk=id_contrato
    )
    context = {}

    if request.method == 'POST':
        form = FiniquitoForm(
            request.POST,
            request.FILES,
        )
        if form.is_valid():
            contrato = form.cleaned_data['contrato']
            razon_baja = form.cleaned_data['contrato']
            descripcion = form.cleaned_data['contrato']
            voto_traslado = form.cleaned_data['contrato']
            documento = form.cleaned_data['documento']

            finiquito = Finiquito.objects.create(
                contrato=contrato,
                razon_baja=razon_baja,
                descripcion=descripcion,
                voto_traslado=voto_traslado,
            )
            Documento.objects.create(
                finiquito=finiquito,
                tipo_documento='finiquito',
                documento=documento,
            )

            contrato.vigente = False
            contrato.save()

            return redirect('rrhh:contrato', finiquito.contrato.pk)

        else:
            # Formulario con errores
            context['message'] = u"Complete la información requerida"
            context['form'] = form

    else:
        form = FiniquitoForm(
            initial={
                'contrato': contrato
            }
        )
        context['form'] = form
        context['funcionario'] = '{} - {}'.format(
            contrato.funcionario.persona.get_full_name,
            contrato.funcion_principal
        )

    return render(
        request,
        'rrhh/finiquito/nuevo_finiquito.html',
        context
    )


class FiniquitoDeleteView(LoginRequiredMixin, DeleteView):
    model = Finiquito

    def get_success_url(self):
        return reverse_lazy(
            'rrhh:contrato',
            kwargs={
                'pk': self.object.contrato.pk,
            }
        )

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class SolicitudListView(LoginRequiredMixin, ListView):
    model = Solicitud
    template_name = 'rrhh/solicitud/listado_solicitud.html'
    search_fields = ['nombre']
    paginate_by = 10


class SolicitudDetailView(LoginRequiredMixin, DetailView):
    model = Solicitud
    template_name = 'rrhh/solicitud/detalle_solicitud.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = EstadoSolicitudForm()
        return context


class SolicitudCreateView(LoginRequiredMixin, CreateView):
    model = Solicitud
    form_class = SolicitudForm
    template_name = 'rrhh/solicitud/nueva_solicitud.html'

    def get_success_url(self):
        EstadoSolicitud.objects.create(
            solicitud=self.object,
            estado=2,
            observaciones='Se crea la solicitud de contratación',
            autor=self.request.user
        )
        return reverse_lazy(
            'rrhh:solicitud',
            kwargs={
                'pk': self.object.pk,
            }
        )


class SolicitudUpdateView(LoginRequiredMixin, UpdateView):
    model = Solicitud
    form_class = SolicitudForm
    template_name = 'rrhh/solicitud/editar_solicitud.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipo'] = self.object.get_tipo_display()
        if self.object.tipo >= 3:
            context['funcionario'] = 'para {}'.format(self.object.contrato.funcionario)
        return context

    def get_success_url(self):
        EstadoSolicitud.objects.create(
            solicitud=self.object,
            estado=2,
            observaciones='Los datos de la solicitud de {}, fueron actualizados'.format(self.object.get_tipo_display()),
            autor=self.request.user
        )
        return reverse_lazy(
            'rrhh:solicitud',
            kwargs={
                'pk': self.object.pk,
            }
        )


class SolicitudDeleteView(LoginRequiredMixin, DeleteView):
    model = Solicitud
    success_url = reverse_lazy('rrhh:solicitudes')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


@login_required
def cambiar_estado_solicitud(request):
    form = EstadoSolicitudForm(request.POST)
    if form.is_valid():
        id_solicitud = request.POST.get('solicitud', None)
        solicitud = get_object_or_404(
            Solicitud,
            id=id_solicitud
        )
        estado = request.POST.get('estado', None)
        voto = request.POST.get('voto', None)
        observaciones = request.POST.get('observaciones', None)

        texto_inicial = 'Se acepta la solicitud de contratación'

        if estado == '2':
            texto_inicial = 'Pendiente de aceptación u observaciones'
        elif estado == '3':
            texto_inicial = 'Se rechaza la solicitud de contratación'
        elif estado == '4':
            texto_inicial = 'En espera de selección de candidatos'
        elif estado == '5':
            texto_inicial = 'Pendiente de aprobación'
        elif estado == '6':
            texto_inicial = 'Se aprueba la solicitud de {} con {} votos'.format(solicitud.get_tipo_display(), voto)

        observaciones_completo = '{}{} {}'.format(
            texto_inicial,
            ', con observaciones: <br>' if observaciones != '' else '',
            observaciones
        )

        es = EstadoSolicitud.objects.create(
            solicitud=solicitud,
            estado=estado,
            voto=voto,
            observaciones=observaciones_completo,
            autor=request.user
        )
        if estado == '1':
            EstadoSolicitud.objects.create(
                solicitud=solicitud,
                estado=4,
                observaciones='En espera de selección de candidatos',
                autor=request.user
            )

        return redirect('rrhh:solicitud', es.solicitud.pk)

    else:
        pass


@login_required
def seleccionar_candidatos(request, id_solicitud):
    context = {}
    postulantes = {p for p in Persona.objects.all() if 'Postulante' in p.clasificacion}

    context['postulantes'] = postulantes
    context['id_solicitud'] = id_solicitud

    return render(
        request,
        'rrhh/solicitud/seleccionar_candidatos.html',
        context
    )


@login_required
@json_view
def guardar_candidato(request):
    persona = get_object_or_404(
        Persona,
        id=request.GET.get('id_persona')
    )
    solicitud = get_object_or_404(
        Solicitud,
        id=request.GET.get('id_solicitud')
    )
    index = request.GET.get('index')

    solicitud.postulantes.add(persona)

    if index == '0':
        EstadoSolicitud.objects.create(
            solicitud=solicitud,
            estado=5,
            observaciones='Pendiente de aprobación <br>Candidatos seleccionados',
            autor=request.user
        )

    return {'mensaje': 'Todo bien'}


@login_required
def crear_contrato(request, id_funcionario, id_solicitud):
    funcionario = get_object_or_404(
        Funcionario,
        id=id_funcionario
    )
    solicitud = get_object_or_404(
        Solicitud,
        id=id_solicitud
    )

    if solicitud.tipo >= 3:
        solicitud.contrato.vigente = False
        solicitud.contrato.save()

    context = crear_contrato_funcion(
        request,
        funcionario,
        solicitud.entidad,
        solicitud.categoria,
        solicitud.tipo_contrato,
        solicitud.reemplazando_licencia,
        solicitud.reemplazando_permiso,
        solicitud.horas,
        solicitud.sueldo,
        solicitud.asignacion_funcion,
        solicitud.asignacion_locomocion,
        solicitud.fecha_inicio,
        solicitud.fecha_termino,
    )

    if context['success']:
        EstadoSolicitud.objects.create(
            solicitud=solicitud,
            estado=7,
            observaciones='Se aprueba y culmina con el contrato de {} en {}'.format(funcionario, solicitud.entidad),
            autor=request.user
        )

        if solicitud.tipo >= 3:
            solicitud.contrato.vigente = True
            solicitud.contrato.save()

        return redirect('rrhh:contrato', context['contrato'].id)

    return render(
        request,
        'rrhh/contrato/nuevo_contrato.html',
        context
    )


@login_required
def renovar_contrato(request, id_contrato):
    contrato = get_object_or_404(
        Contrato,
        id=id_contrato
    )

    context = crear_solicitud_funcion(
        request,
        3,
        contrato.entidad,
        contrato,
        contrato.categoria,
        contrato.horas_total,
        contrato.sueldo,
        contrato.asignacion_funcion,
        contrato.asignacion_locomocion,
        contrato.tipo_contrato,
        None,
        None,
        contrato.fecha_termino,
        None,
        'Renovación de contrato',
    )

    if context['success']:
        EstadoSolicitud.objects.create(
            solicitud=context['solicitud'],
            estado=2,
            observaciones='Se crea la solicitud de renovación de contrato',
            autor=request.user
        )
        return redirect('rrhh:solicitud', context['solicitud'].id)

    return render(
        request,
        'rrhh/solicitud/nueva_solicitud.html',
        context
    )


@login_required
def trasladar_funcionario(request, id_contrato):
    contrato = get_object_or_404(
        Contrato,
        id=id_contrato
    )

    context = crear_solicitud_funcion(
        request,
        4,
        None,
        contrato,
        contrato.categoria,
        contrato.horas_total,
        contrato.sueldo,
        contrato.asignacion_funcion,
        contrato.asignacion_locomocion,
        contrato.tipo_contrato,
        None,
        None,
        contrato.fecha_inicio,
        contrato.fecha_termino,
        'Se traslada al Docente',
    )

    if context['success']:
        EstadoSolicitud.objects.create(
            solicitud=context['solicitud'],
            estado=2,
            observaciones='Se crea la solicitud de traslado',
            autor=request.user
        )
        return redirect('rrhh:solicitud', context['solicitud'].id)

    return render(
        request,
        'rrhh/solicitud/nueva_solicitud.html',
        context
    )


def crear_solicitud_funcion(
        request,
        tipo_solicitud,
        entidad,
        contrato,
        categoria,
        horas,
        sueldo,
        asignacion_funcion,
        asignacion_locomocion,
        tipo_contrato,
        licencia,
        permiso,
        fecha_inicio,
        fecha_termino,
        justificacion,
):
    context = {
        'success': False
    }

    if request.method == 'POST':
        form = SolicitudForm(request.POST)
        if form.is_valid():
            solicitud = form.save()

            context['success'] = True
            context['solicitud'] = solicitud
        else:
            context['form'] = form
            context['menssge'] = 'El Formulario no es válido'

    else:
        form = SolicitudForm(
            initial={
                'tipo': tipo_solicitud,
                'entidad': entidad,
                'contrato': contrato,
                'categoria': categoria,
                'horas': horas,
                'sueldo': sueldo,
                'asignacion_funcion': asignacion_funcion,
                'asignacion_locomocion':asignacion_locomocion,
                'tipo_contrato': tipo_contrato,
                'remmplazando_licencia': licencia,
                'remmplazando_permiso': permiso,
                'fecha_inicio': fecha_inicio,
                'fecha_termino': fecha_termino,
                'justificacion': justificacion,
            }
        )

        tipos = ['Contratación', 'Contratación de reemplazo', 'Renovación de contrato', 'Traslado']
        context['form'] = form
        context['funcionario'] = 'para {}'.format(contrato.funcionario)
        context['tipo'] = tipos[tipo_solicitud - 1]

    return context


def crear_contrato_funcion(
        request,
        funcionario,
        entidad,
        categoria,
        tipo_contrato,
        licencia,
        permiso,
        horas_total,
        sueldo,
        asignacion_funcion,
        asignacion_locomocion,
        fecha_inicio,
        fecha_termino,
):
    context = {
        'success': False
    }

    if request.method == 'POST':
        form = ContratoForm(request.POST)
        if form.is_valid():
            c = form.save()

            EstadoContratacion.objects.create(
                contrato=c,
                estado=1,
                observaciones='Se inicia el proceso de contratación,'
                              'el cual permitirá la creación, revisión y carga del contrato del trabajador',
                autor=request.user
            )
            context['success'] = True
            context['contrato'] = c
        else:
            # Formulario con errores
            context['message'] = u"Complete la información requerida"
            context['form'] = form

    else:
        form = ContratoForm(
            initial={
                'funcionario': funcionario,
                'entidad': entidad,
                'categoria': categoria,
                'tipo_contrato': tipo_contrato,
                'reemplazando_licencia': licencia,
                'reemplazando_permiso': permiso,
                'horas_total': horas_total,
                'sueldo': sueldo,
                'asignacion_funcion': asignacion_funcion,
                'asignacion_locomocion': asignacion_locomocion,
                'fecha_inicio': fecha_inicio,
                'fecha_termino': fecha_termino,
            },
        )
        context['form'] = form

    return context


@login_required
def cambiar_estado_contratacion(request):
    form = EstadoContratacionForm(request.POST, request.FILES)
    if form.is_valid():
        contrato = get_object_or_404(
            Contrato,
            pk=request.POST.get('contrato')
        )
        estado = request.POST.get('estado')
        observaciones = request.POST.get('observaciones')

        texto_inicial = 'El Contrato esta listo para ser descargado y firmado'

        if estado == '3':
            texto_inicial = 'Se debe revisar nuevamente el contrato'
        elif estado == '4':
            texto_inicial = 'Se aprueba y firma el contrato'
            Documento.objects.create(
                contrato=contrato,
                tipo_documento='contrato',
                documento=request.FILES['documento']
            )
            contrato.vigente = True
            contrato.save()

        observaciones_completo = '{}{} {}'.format(
            texto_inicial,
            ', con observaciones: <br>' if observaciones != '' else '',
            observaciones
        )

        EstadoContratacion.objects.create(
            contrato=contrato,
            estado=estado,
            observaciones=observaciones_completo,
            autor=request.user
        )

        return redirect('rrhh:contrato', contrato.pk)

    else:
        print(form.errors)


@login_required
def cargar_documento_personal(request):
    if request.method == 'POST':
        form = DocumentoForm(request.POST, request.FILES)
        
        if form.is_valid():
            contrato = form.cleaned_data['contrato']
            documento = form.cleaned_data['documento']
            tipo_documento = 'otro'
            if 'cargar_contrato_pdf' in request.POST:
                tipo_documento = 'contrato'
            if 'cargar_reglamento_pdf' in request.POST:
                tipo_documento = 'conocimiento reglamento'
            if 'cargar_diezmo_pdf' in request.POST:
                tipo_documento = 'autorizacion diezmo'
            if 'cargar_imagen_pdf' in request.POST:
                tipo_documento = 'autorizacion imagen'
            if request.POST['tipo_documento'] == 'contrato':
                tipo_documento = 'contrato'
            if request.POST['tipo_documento'] == 'conocimiento reglamento':
                tipo_documento = 'conocimiento reglamento'
            if request.POST['tipo_documento'] == 'autorizacion diezmo':
                tipo_documento = 'autorizacion diezmo'
            if request.POST['tipo_documento'] == 'autorizacion imagen':
                tipo_documento = 'autorizacion imagen' 

            d = Documento.objects.create(
                contrato=contrato,
                tipo_documento=tipo_documento,
                documento=documento
            )

            return redirect('rrhh:contrato', d.contrato.pk)
