import io
import zipfile

import xlsxwriter
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from guardian.shortcuts import assign_perm
from guardian.shortcuts import remove_perm
from wkhtmltopdf.views import PDFTemplateResponse

from carga_horaria.formsDani import PeriodoForm, ColegioForm, PlanForm
from carga_horaria.models import Plan
from . import models
from .forms import AsignacionAsistenteForm
from .forms import AsignacionExtraForm
from .forms import AsignacionExtraUpdateForm
from .forms import AsignacionFUAForm
from .forms import AsignacionForm
from .forms import AsignacionNoAulaFUAForm
from .forms import AsignacionNoAulaForm
from .forms import AsignacionNoAulaUpdateForm
from .forms import AsignacionUpdateForm
from .forms import AssignPermForm
from .formsDani import PlantillaPlanForm
from .models import Asignacion
from .models import AsignacionAsistente
from .models import AsignacionExtra
from .models import AsignacionNoAula
from .viewsAlexis import *


@login_required
def assign(request):
    if not request.user.is_superuser:
        raise Http404

    year = request.session.get('periodo', 2020)
    if request.method == 'POST':
        form = AssignPermForm(request.POST, year=year)
        if form.is_valid():
            user = form.cleaned_data['usuario']

            # clear perms first
            remove_perm('carga_horaria.change_colegio', user, get_objects_for_user(user, 'carga_horaria.change_colegio').filter(periode=year))

            for c in form.cleaned_data['colegios']:
                assign_perm('change_colegio', user, c)
        
    form = AssignPermForm(year=year)
    return render(request, 'carga_horaria/assign.html', {'form': form})



@login_required
def switch_periodo(request, year=2021):
    request.session['periodo'] = year
    try:
        del request.session['colegio__pk']
        del request.session['colegio__nombre']
    except KeyError:
        pass
    return redirect('carga-horaria:home')

@login_required
def switch(request, pk=None):
    if pk:
        colegio = get_object_or_404(Colegio, pk=pk)
        request.session['colegio__pk'] = colegio.pk
        request.session['colegio__nombre'] = colegio.nombre
        return redirect('carga-horaria:home')
    colegios = get_objects_for_user(request.user, "carga_horaria.change_colegio", Colegio.objects.filter(periode=request.session.get('periodo', 2020)))
    return render(request, 'carga_horaria/switch.html', {'colegios': colegios})

@login_required
def clear(request):
    del request.session['colegio__pk']
    del request.session['colegio__nombre']
    return redirect('carga-horaria:home')

@login_required
def home(request):
    return render(request, 'carga_horaria/home.html')



@login_required
def anexo(request, pk):
    p = get_object_or_404(Profesor, pk=pk)
    colegio = Colegio.objects.get(pk=request.session['colegio__pk'])
    response = PDFTemplateResponse(request=request,
                                   template='carga_horaria/profesor/anexo_profesor.html',
                                   filename='anexo1.pdf',
                                   context={'profesor': p,
                                            'colegio': colegio,
                                            'periodo': request.session.get('periodo', 2020)},
                                   show_content_in_browser=settings.DEBUG)
    return response

@login_required
def anexos(request):
    profesores = get_for_user(request, Profesor.objects.all(), 'colegio__pk', request.user)
    mem_zip = io.BytesIO()
    with zipfile.ZipFile(mem_zip, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        for pp in profesores:
            zf.writestr(*pp.generar_anexo_1())

    response = HttpResponse(mem_zip.getvalue(), content_type='applicaton/zip')
    response['Content-Disposition'] = 'attachment; filename="anexos1.zip"'
    return response


@login_required
def anexo_asistente(request, pk):
    p = get_object_or_404(Asistente, pk=pk)
    colegio = Colegio.objects.get(pk=request.session['colegio__pk'])
    response = PDFTemplateResponse(request=request,
                                   template='carga_horaria/asistente/anexo_asistente.html',
                                   filename='anexo1.pdf',
                                   context={'profesor': p,
                                            'colegio': colegio,
                                            'periodo': request.session.get('periodo', 2020)},
                                   show_content_in_browser=settings.DEBUG)
    return response

@login_required
def anexos_asistentes(request):
    profesores = get_for_user(request, Asistente.objects.all(), 'colegio__pk', request.user)
    mem_zip = io.BytesIO()
    with zipfile.ZipFile(mem_zip, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        for pp in profesores:
            zf.writestr(*pp.generar_anexo_1())

    response = HttpResponse(mem_zip.getvalue(), content_type='applicaton/zip')
    response['Content-Disposition'] = 'attachment; filename="anexos1.zip"'
    return response


@login_required
def profesores_pdf(request):
    profesores = get_for_user(request, Profesor.objects.all(), 'colegio__pk', request.user)
    response = PDFTemplateResponse(request=request,
                                   template='carga_horaria/profesor/listado_profesor_pdf.html',
                                   filename='listado_profesores.pdf',
                                   context={'profesores': profesores},
                                   show_content_in_browser=settings.DEBUG)
    return response


@login_required
def asistentes_pdf(request):
    asistentes = get_for_user(request, Asistente.objects.all(), 'colegio__pk', request.user)
    response = PDFTemplateResponse(request=request,
                                   template='carga_horaria/asistente/listado_asistente_pdf.html',
                                   filename='listado_asistentes.pdf',
                                   context={'asistentes': asistentes},
                                   show_content_in_browser=settings.DEBUG)
    return response

@login_required
def periodo_pdf(request, pk):
    periodo = get_object_or_404(Periodo, pk=pk)
    response = PDFTemplateResponse(request=request,
                                   template='carga_horaria/periodo/periodo_pdf.html',
                                   filename='carga_horaria.pdf',
                                   context={'object': periodo},
                                   show_content_in_browser=settings.DEBUG)
    return response

@login_required
def plan_refresh(request, pk):
    plan = get_object_or_404(Plan, pk=pk)
    plan.refresh_asignaturas()
    messages.success(request, "Se han actualizado los cursos asociados al plan ID: {}".format(plan.pk))
    return redirect('carga-horaria:planes')

# class AnexoView(PDFTemplateView):
#     template_name = 'carga_horaria/profesor/anexo_profesor.html'
#     filename = 'anexo1.pdf'

#     def get(self, request, *args, **kwargs):
#         pk = kwargs.pop('pk')
#         self.p = get_object_or_404(Profesor, pk=pk)
#         self.ax = [{'descripcion': 'Planificación', 'curso': '', 'horas': self.p.horas_planificacion},
#                    {'descripcion': 'Recreo', 'curso': '', 'horas': self.p.horas_recreo}] + list(self.p.asignacionextra_set.all())
#         return super(AnexoView, self).get(request, *args, **kwargs)

#     def get_context_data(self, *args, **kwargs):
#         ctx = super(AnexoView, self).get_context_data(*args, **kwargs)
#         ctx.update({'asignaciones': self.p.asignacion_set.all(),
#                     'asignaciones_extra': self.ax,
#                     'profesor': self.p})

# anexo = AnexoView.as_view()


"""
    Comienzo Crud Periodos
"""
class PeriodoListView(LoginRequiredMixin, GetObjectsForUserMixin, ListView):
    """
        Listado de periodos
    """
    model = Periodo
    lookup = 'colegio__pk'
    template_name = 'carga_horaria/periodo/listado_periodos.html'
    search_fields = ['nombre', 'colegio']
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        ctx = super(PeriodoListView, self).get_context_data(*args, **kwargs)
        ox = ctx['object_list']
        ordering = {str(value): index for index, value in enumerate(Nivel)}
        ctx['object_list'] = sorted(ox, key=lambda x: ordering["Nivel."+x.plan.nivel])
        # added for convenience, pasted from AsignaturaBaseListView
        ctx['levels'] = [(tag.name, tag.value) for tag in Nivel]
        ctx['nivel_actual'] = self.request.GET.get('nivel')
        return ctx

    def get_queryset(self):
        qs = super().get_queryset()

        nivel = self.request.GET.get('nivel')
        if nivel:
            qs = qs.filter(plan__nivel=nivel)

        return qs




class PeriodoDetailView(LoginRequiredMixin, DetailView):
    """
        Detalle de Periodo
    """
    model = Periodo
    template_name = 'carga_horaria/periodo/detalle_periodo.html'


class PeriodoCreateView(LoginRequiredMixin, CreateView):
    model = Periodo
    form_class = PeriodoForm
    template_name = 'carga_horaria/periodo/nuevo_periodo.html'
    success_url = reverse_lazy('carga-horaria:periodos')

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(PeriodoCreateView, self).get_form_kwargs(*args, **kwargs)
        kwargs.update({'user': self.request.user,
                       'colegio': self.request.session.get('colegio__pk', None)})
        return kwargs


class PeriodoUpdateView(LoginRequiredMixin, UpdateView):
    model = Periodo
    form_class = PeriodoForm
    template_name = 'carga_horaria/periodo/editar_periodo.html'

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(PeriodoUpdateView, self).get_form_kwargs(*args, **kwargs)
        kwargs.update({'user': self.request.user,
                       'colegio': self.request.session.get('colegio__pk', None)})
        return kwargs

    def get_success_url(self):
        return reverse(
            'carga-horaria:periodo',
            kwargs={
                'pk': self.object.pk,
            }
        )


class PeriodoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Periodo
    success_url = reverse_lazy('carga-horaria:periodos')
    template_name = 'carga_horaria/periodo/eliminar_periodo.html'

    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
"""
    Fin Crud Periodos
"""

"""
    Comienzo Crud Colegios
"""
class ColegioListView(LoginRequiredMixin, GetObjectsForUserMixin, ListView):
    """
        Listado de periodos
    """
    model = Colegio
    lookup = 'pk'
    template_name = 'carga_horaria/colegio/listado_colegios.html'
    search_fields = ['nombre', 'jec']
    paginate_by = 6


class ColegioDetailView(LoginRequiredMixin, ObjPermissionRequiredMixin, DetailView):
    """
        Detalle de Colegio
    """
    model = Colegio
    permission = 'carga_horaria.change_colegio'
    template_name = 'carga_horaria/colegio/detalle_colegio.html'


class ColegioCreateView(LoginRequiredMixin, CreateView):
    model = Colegio
    form_class = ColegioForm
    template_name = 'carga_horaria/colegio/nuevo_colegio.html'
    success_url = reverse_lazy('carga-horaria:colegios')
#    success_message = u"Nuevo periodo %(nombre)s creado satisfactoriamente."
#    error_message = "Revise que todos los campos del formulario hayan sido validados correctamente."

    def form_valid(self, form):
        colegio = form.save(commit=False)
        colegio.periode = self.request.session.get('periodo', 2020)
        colegio.save()
        return redirect(reverse('carga-horaria:colegios'))


class ColegioUpdateView(LoginRequiredMixin, UpdateView):
    model = Colegio
    form_class = ColegioForm
    template_name = 'carga_horaria/colegio/editar_colegio.html'

    def get_success_url(self):
        return reverse(
            'carga-horaria:colegio',
            kwargs={
                'pk': self.object.pk,
            }
        )



class ColegioDeleteView(LoginRequiredMixin, DeleteView):
    model = Colegio
    success_url = reverse_lazy('carga-horaria:colegios')
    
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


"""
    Fin Crud Colegios
"""

"""
    Comienzo Crud Planes
"""
class PlanListView(LoginRequiredMixin, GetObjectsForUserMixin, ListView):
    """
        Listado de planes
    """
    model = Plan
    lookup = 'colegio__pk'
    template_name = 'carga_horaria/plan/listado_planes.html'
    search_fields = ['nombre', 'nivel']
    paginate_by = 10
    ordering = ['-pk']


class PlanDetailView(LoginRequiredMixin, DetailView):
    """
        Detalle de Plan
    """
    model = Plan
    template_name = 'carga_horaria/plan/detalle_plan.html'


class PlanCreateView(LoginRequiredMixin, CreateView):
    model = Plan
    form_class = PlanForm
    template_name = 'carga_horaria/plan/nuevo_plan.html'
    success_url = reverse_lazy('carga-horaria:planes')
#    success_message = u"Nuevo periodo %(nombre)s creado satisfactoriamente."
#    error_message = "Revise que todos los campos del formulario hayan sido validados correctamente."

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(PlanCreateView, self).get_form_kwargs(*args, **kwargs)
        kwargs.update({'user': self.request.user,
                       'colegio': self.request.session.get('colegio__pk', None)})
        return kwargs


@login_required
def crear_desde_plantilla(request):
    if request.method == 'POST':
        form = PlantillaPlanForm(request.POST)
        if form.is_valid():
            plantilla = form.cleaned_data['plantilla']
            nivel = form.cleaned_data['nivel']

            colegio_pk = request.session.get('colegio__pk', None)
            if colegio_pk:
                colegio = Colegio.objects.get(pk=colegio_pk)
                nuevo = Plan.objects.create(nivel=nivel, colegio=colegio)
            else:
                nuevo = Plan.objects.create(nivel=nivel)
            for ab in plantilla.asignaturabase_set.all():
                AsignaturaBase.objects.create(nombre=ab.nombre,
                                              plan=nuevo,
                                              horas_jec=ab.horas_jec,
                                              horas_nec=ab.horas_nec)
            return redirect('carga-horaria:planes')
    else:
        form = PlantillaPlanForm()
    return render(request, 'carga_horaria/plantilla.html', {'form': form})


class PlanUpdateView(LoginRequiredMixin, UpdateView):
    model = Plan
    form_class = PlanForm
    template_name = 'carga_horaria/plan/editar_plan.html'

    def get_success_url(self):
        return reverse(
            'carga-horaria:plan',
            kwargs={
                'pk': self.object.pk,
            }
        )


class PlanDeleteView(LoginRequiredMixin, DeleteView):
    model = Plan
    success_url = reverse_lazy('carga-horaria:planes')
    template_name = 'carga_horaria/plan/eliminar_plan.html'
    
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
"""
    Fin Crud Planes
"""

@login_required
def asignatura_limpiar(request, pk, periodo_pk):
    aa = get_object_or_404(Asignatura, pk=pk)
    aa.asignacion_set.all().delete()
    return redirect(reverse('carga-horaria:periodo', kwargs={'pk': periodo_pk}))


@login_required
def asignatura_dif(request, pk):
    pp = get_object_or_404(Periodo, pk=pk)

    if request.method == 'POST':
        # check first if there are any candidates for merging
        nombre = request.POST['asignatura']
        colegio_pk = request.session.get('colegio__pk', None)
        can_confirm = request.POST.get('can_confirm', False)
        if colegio_pk and Asignatura.objects.filter(periodos__colegio=colegio_pk, nombre=nombre) and not can_confirm:
            ax = Asignatura.objects.filter(periodos__colegio=colegio_pk, nombre=nombre).distinct()
            return render(request, 'carga_horaria/asignatura/asignatura_dif_confirm.html', {'object': pp,
                                                                                            'candidatas': ax})
        else:
            aa = Asignatura.objects.create(nombre=request.POST['asignatura'],
                                           diferenciada=True,
                                           horas=6)
            aa.periodos.add(pp)
            return redirect('carga-horaria:periodo', pp.pk)
    return render(request, 'carga_horaria/asignatura/asignatura_dif.html', {'object': pp})


@login_required
def asignatura_merge(request, pk, asignatura_pk):
    pp = get_object_or_404(Periodo, pk=pk)
    aa = get_object_or_404(Asignatura, pk=asignatura_pk)
    aa.periodos.add(pp)
    return redirect('carga-horaria:periodo', pk)


@login_required
def asignatura_maybe(request, pk):
    pp = get_object_or_404(Periodo, pk=pk)
    candidatas = Asignatura.objects.filter(periodos__colegio=pp.colegio, combinable=True).exclude(periodos__pk__in=[pk]).distinct()
    if candidatas:
        return render(request, 'carga_horaria/asignatura/asignatura_maybe.html', {'object': pp, 'candidatas': candidatas})
    else:
        return redirect('carga-horaria:asignatura__nuevo', pk)


@login_required
def asignar(request, pk, periodo_pk):
    aa = get_object_or_404(Asignatura, pk=pk)

    if request.method == 'POST':
        form = AsignacionForm(request.POST, asignatura=aa, user=request.user, colegio=request.session.get('colegio__pk', None), periodo=request.session.get('periodo', 2020))
        if form.is_valid():
            asignacion = form.save(commit=False)
            asignacion.asignatura = aa
            asignacion.save()
            return redirect('carga-horaria:periodo', periodo_pk)
    else:
        form = AsignacionForm(user=request.user, colegio=request.session.get('colegio__pk', None))
    return render(request, 'carga_horaria/asignar.html', {'object': aa,
                                                          'form': form})


@login_required
def asignar_fua(request, pk, tipo):
    pp = get_object_or_404(Profesor, pk=pk)
    tipo_display = dict(Asignacion.TIPO_CHOICES)[int(tipo)]

    if request.method == 'POST':
        form = AsignacionFUAForm(request.POST, profesor=pp, user=request.user, colegio=request.session.get('colegio__pk', None), periodo=request.session.get('periodo', 2020))
        if form.is_valid():
            asignacion = form.save(commit=False)
            asignacion.profesor = pp
            asignacion.tipo = tipo
            asignacion.save()
            return redirect('carga-horaria:profesor', pp.pk)
    else:
        form = AsignacionFUAForm(user=request.user, colegio=request.session.get('colegio__pk', None))
    return render(request, 'carga_horaria/asignar_fua.html', {'object': pp,
                                                              'tipo': tipo_display,
                                                              'form': form})

@login_required
def asignar_no_aula_fua(request, pk, tipo):
    pp = get_object_or_404(Profesor, pk=pk)
    tipo_display = dict(AsignacionNoAula.TIPO_CHOICES)[int(tipo)]

    if request.method == 'POST':
        form = AsignacionNoAulaFUAForm(request.POST, profesor=pp, user=request.user, colegio=request.session.get('colegio__pk', None), periodo=request.session.get('periodo', 2020))
        if form.is_valid():
            asignacion = form.save(commit=False)
            asignacion.profesor = pp
            asignacion.tipo = tipo
            if asignacion.horas == 0:
                asignacion.horas = pp.horas_no_aula_disponibles
            asignacion.save()
            return redirect('carga-horaria:profesor', pp.pk)
    else:
        form = AsignacionNoAulaFUAForm(user=request.user, colegio=request.session.get('colegio__pk', None))
    return render(request, 'carga_horaria/asignar_no_aula_fua.html', {'profesor': pp,
                                                                      'tipo': tipo_display,
                                                                      'form': form})



@login_required
def asignar_extra(request, pk):
    pp = get_object_or_404(Profesor, pk=pk)

    if request.method == 'POST':
        form = AsignacionExtraForm(request.POST, profesor=pp, user=request.user, colegio=request.session.get('colegio__pk', None), periodo=request.session.get('periodo', 2020))
        if form.is_valid():
            asignacion = form.save(commit=False)
            asignacion.profesor = pp
            if asignacion.horas == 0:
                asignacion.horas = pp.horas_no_lectivas_disponibles
            asignacion.save()
            return redirect('carga-horaria:profesor', pp.pk)
    else:
        form = AsignacionExtraForm(user=request.user, colegio=request.session.get('colegio__pk', None))
    return render(request, 'carga_horaria/asignar_extra.html', {'profesor': pp,
                                                                'form': form})


@login_required
def asignar_no_aula(request, pk):
    pp = get_object_or_404(Profesor, pk=pk)

    if request.method == 'POST':
        form = AsignacionNoAulaForm(request.POST, profesor=pp, user=request.user, colegio=request.session.get('colegio__pk', None), periodo=request.session.get('periodo', 2020))
        if form.is_valid():
            asignacion = form.save(commit=False)
            asignacion.profesor = pp
            if asignacion.horas == 0:
                asignacion.horas = pp.horas_no_aula_disponibles
            asignacion.save()
            return redirect('carga-horaria:profesor', pp.pk)
    else:
        form = AsignacionNoAulaForm(user=request.user, colegio=request.session.get('colegio__pk', None))
    return render(request, 'carga_horaria/asignar_no_aula.html', {'profesor': pp,
                                                                  'form': form})

class AsignacionDeleteView(LoginRequiredMixin, DeleteView):
    model = Asignacion
    template_name = 'carga_horaria/periodo/eliminar_periodo.html'

    def get_success_url(self):
        return reverse('carga-horaria:profesor', kwargs={'pk': self.kwargs['profesor_pk']})

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class AsignacionUpdateView(LoginRequiredMixin, UpdateView):
    model = Asignacion
    form_class = AsignacionUpdateForm
    template_name = 'carga_horaria/asignar_update.html'


    def get_success_url(self):
        return reverse(
            'carga-horaria:profesor',
            kwargs={
                'pk': self.object.profesor.pk,
            }
        )


class AsignacionExtraUpdateView(LoginRequiredMixin, UpdateView):
    model = AsignacionExtra
    form_class = AsignacionExtraUpdateForm
    template_name = 'carga_horaria/asignar_extra.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super(AsignacionExtraUpdateView, self).get_context_data(*args, **kwargs)
        ctx['profesor'] = self.object.profesor
        return ctx

    def get_form_kwargs(self, *args, **kwargs):
        pp = get_object_or_404(Profesor, pk=self.kwargs.get('profesor_pk'))

        kwargs = super(AsignacionExtraUpdateView, self).get_form_kwargs(*args, **kwargs)
        kwargs.update({'profesor': pp,
                       'user': self.request.user,
                       'colegio': self.request.session.get('colegio__pk', None)})
        return kwargs

    def form_valid(self, form):
        asignacion = form.save(commit=False)
        if asignacion.horas == 0:
            asignacion_old = Asignacion.objects.get(pk=asignacion.pk)
            asignacion.horas = asignacion.profesor.horas_no_lectivas_disponibles + float(asignacion_old.horas)
        asignacion.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse(
            'carga-horaria:profesor',
            kwargs={
                'pk': self.object.profesor.pk,
            }
        )


class AsignacionExtraDeleteView(LoginRequiredMixin, DeleteView):
    model = AsignacionExtra
    template_name = 'carga_horaria/periodo/eliminar_periodo.html'

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse(
            'carga-horaria:profesor',
            kwargs={
                'pk': self.object.profesor.pk,
            }
        )


class AsignacionNoAulaUpdateView(LoginRequiredMixin, UpdateView):
    model = AsignacionNoAula
    form_class = AsignacionNoAulaUpdateForm
    template_name = 'carga_horaria/asignar_no_aula.html'

    def form_valid(self, form):
        asignacion = form.save(commit=False)
        if asignacion.horas == 0:
            asignacion_old = AsignacionNoAula.objects.get(pk=asignacion.pk)
            asignacion.horas = asignacion.profesor.horas_no_aula_disponibles + asignacion_old.horas
        asignacion.save()
        return redirect(self.get_success_url())

    def get_context_data(self, *args, **kwargs):
        ctx = super(AsignacionNoAulaUpdateView, self).get_context_data(*args, **kwargs)
        ctx['profesor'] = self.object.profesor
        return ctx

    def get_form_kwargs(self, *args, **kwargs):
        pp = get_object_or_404(Profesor, pk=self.kwargs.get('profesor_pk'))

        kwargs = super(AsignacionNoAulaUpdateView, self).get_form_kwargs(*args, **kwargs)
        kwargs.update({'profesor': pp,
                       'user': self.request.user,
                       'colegio': self.request.session.get('colegio__pk', None)})
        return kwargs

    def get_success_url(self):
        return reverse(
            'carga-horaria:profesor',
            kwargs={
                'pk': self.object.profesor.pk,
            }
        )

class AsignacionNoAulaDeleteView(LoginRequiredMixin, DeleteView):
    model = AsignacionNoAula
    template_name = 'carga_horaria/periodo/eliminar_periodo.html'

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse(
            'carga-horaria:profesor',
            kwargs={
                'pk': self.object.profesor.pk,
            }
        )


@login_required
def asignar_asistente(request, pk, tipo):
    pp = get_object_or_404(Asistente, pk=pk)
    tipo_display = dict(AsignacionAsistente.TIPO_CHOICES)[int(tipo)]

    if request.method == 'POST':
        form = AsignacionAsistenteForm(request.POST, asistente=pp, user=request.user, colegio=request.session.get('colegio__pk', None), periodo=request.session.get('periodo', 2020))
        if form.is_valid():
            asignacion = form.save(commit=False)
            asignacion.asistente = pp
            asignacion.tipo = tipo
            # if asignacion.horas == 0:
            #     asignacion.horas = pp.horas_no_lectivas_disponibles
            asignacion.save()
            return redirect('carga-horaria:asistente', pp.pk)
    else:
        form = AsignacionAsistenteForm(user=request.user, colegio=request.session.get('colegio__pk', None))
    return render(request, 'carga_horaria/asignar_asistente.html', {'asistente': pp,
                                                                'form': form})

class AsignacionAsistenteDeleteView(LoginRequiredMixin, DeleteView):
    model = AsignacionAsistente
    template_name = 'carga_horaria/periodo/eliminar_periodo.html'

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse(
            'carga-horaria:asistente',
            kwargs={
                'pk': self.object.asistente.pk,
            }
        )

@login_required
def profesores_info(request):
    output = io.BytesIO()

    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet('Profesores')
    
    # Some data we want to write to the worksheet.
    qs = get_for_user(request, Profesor.objects.all(), 'colegio__pk', request.user)

    # Start from the first cell. Rows and columns are zero indexed.
    row = 0
    col = 0

    # Iterate over the data and write it out row by row.
    worksheet.write(0, 0, 'RUT')
    worksheet.write(0, 1, 'Nombre Docente')
    worksheet.write(0, 2, 'Dirección Docente')
    worksheet.write(0, 3, 'Comuna')
    worksheet.write(0, 4, 'Nacionalidad')
    worksheet.write(0, 5, 'Teléfono')
    worksheet.write(0, 6, 'Email personal')
    worksheet.write(0, 7, 'Email institucional')
    worksheet.write(0, 8, 'Estado civil')
    worksheet.write(0, 9, 'Discapacidad')
    worksheet.write(0, 10, 'Recibe pensión')
    worksheet.write(0, 11, 'Adventista')
    worksheet.write(0, 12, 'Fecha de Nacimiento')
    worksheet.write(0, 13, 'Tipo de Contrato')
    worksheet.write(0, 14, 'Cargo')
    worksheet.write(0, 15, 'Fecha de Inicio Contrato')
    worksheet.write(0, 16, 'Horas Contrato Propuestas')
    worksheet.write(0, 17, 'Horas SBVG')
    worksheet.write(0, 18, 'Horas SEP')
    worksheet.write(0, 19, 'Horas PIE')
    worksheet.write(0, 20, 'Horas Indefinidas Actual')
    worksheet.write(0, 21, 'Horas Plazo Fijo Actual')
    worksheet.write(0, 22, 'Horas Jornada Semanal')
    worksheet.write(0, 23, 'Asignaciones Aula Plan')
    worksheet.write(0, 24, 'Horas Aula PIE')
    worksheet.write(0, 25, 'Horas Aula SEP')
    worksheet.write(0, 26, 'Horas Aula Sostenedor')
    worksheet.write(0, 27, 'Horas disponibles')
    worksheet.write(0, 28, 'Asignación No Lectiva')
    worksheet.write(0, 29, 'Horas no lectivas disponibles')
    worksheet.write(0, 30, 'Asignación No Aula Normal')
    worksheet.write(0, 31, 'Asignación No Aula PIE')
    worksheet.write(0, 32, 'Asignación No Aula SEP')
    worksheet.write(0, 33, 'Especialidad')
    worksheet.write(0, 34, 'Profesor Jefe')
    worksheet.write(0, 35, 'Colegio')
    worksheet.write(0, 36, 'Fundación que lo contrata')
  


    
    row = 1
    for pp in qs:
        worksheet.write(row, 0, pp.rut)
        worksheet.write(row, 1, pp.nombre)
        worksheet.write(row, 2, pp.direccion)
        worksheet.write(row, 3, pp.persona.comuna)
        worksheet.write(row, 4, pp.persona.nacionalidad)
        worksheet.write(row, 5, pp.persona.telefono)
        worksheet.write(row, 6, pp.persona.email_personal)
        worksheet.write(row, 7, pp.persona.email_institucional)
        worksheet.write(row, 8, pp.persona.get_estado_civil_display())
        worksheet.write(row, 9, 'Sí' if pp.persona.discapacidad else 'No')
        worksheet.write(row, 10, 'Sí' if pp.persona.recibe_pension else 'No')
        worksheet.write(row, 11, 'Sí' if pp.persona.adventista else 'No')
        worksheet.write(row, 12, pp.persona.fecha_nacimiento)
        worksheet.write(row, 13, pp.get_tipo_display())
        worksheet.write(row, 14, pp.get_cargo_display())
        worksheet.write(row, 15, pp.fecha_inicio)
        worksheet.write(row, 16, pp.horas_semanales_total)
        worksheet.write(row, 17, pp.horas_sbvg_total)
        worksheet.write(row, 18, pp.total_sep)
        worksheet.write(row, 19, pp.total_pie)
        worksheet.write(row, 20, pp.horas_indefinidas)
        worksheet.write(row, 21, pp.horas_plazo_fijo)
        worksheet.write(row, 22, pp.horas_semanales)
        worksheet.write(row, 23, pp.horas_asignadas_plan)
        worksheet.write(row, 24, pp.horas_asignadas_pie)
        worksheet.write(row, 25, pp.horas_asignadas_sep)
        worksheet.write(row, 26, pp.horas_asignadas_sostenedor)
        worksheet.write(row, 27, pp.horas_disponibles)
        worksheet.write(row, 28, pp.horas_no_lectivas_asignadas_anexo)
        worksheet.write(row, 29, pp.horas_no_lectivas_disponibles)
        worksheet.write(row, 30, pp.horas_no_aula_asignadas_ordinaria)
        worksheet.write(row, 31, pp.horas_no_aula_asignadas_pie)
        worksheet.write(row, 32, pp.horas_no_aula_asignadas_sep)
        worksheet.write(row, 33, str(pp.especialidad))
        worksheet.write(row, 34, pp.jefatura if pp.es_profesor_jefe else 'No')
        worksheet.write(row, 35, str(pp.colegio))
        worksheet.write(row, 36, str(pp.fundacion))

        row += 1

    workbook.close()
    output.seek(0)

    # Set up the Http response.
    filename = 'profesores-info.xlsx'
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response


@login_required
def profesores_auto(request):
    output = io.BytesIO()

    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet('Profesores')
    
    # Some data we want to write to the worksheet.
    qs = get_for_user(request, Profesor.objects.all(), 'colegio__pk', request.user)

    # Start from the first cell. Rows and columns are zero indexed.
    row = 0
    col = 0

    # Iterate over the data and write it out row by row.
    worksheet.write(0, 0, 'RUT Evaluador')
    worksheet.write(0, 1, 'Nombres Evaluador')
    worksheet.write(0, 2, 'Correo Institucional Evaluador')
    worksheet.write(0, 3, 'Función Evaluador')
    worksheet.write(0, 4, 'Colegio Evaluador')
    worksheet.write(0, 5, 'Fundación Evaluador')
    worksheet.write(0, 6, 'RUT Evaluado')
    worksheet.write(0, 7, 'Nombres Evaluado')
    worksheet.write(0, 8, 'Correo Institucional Evaluado')
    worksheet.write(0, 9, 'Función Evaluado')
    worksheet.write(0, 10, 'Colegio Evaluado')
    worksheet.write(0, 11, 'Fundación Evaluado')


    row = 1
    for pp in qs:
        worksheet.write(row, 0, pp.rut)
        worksheet.write(row, 1, pp.nombre)
        worksheet.write(row, 2, pp.persona.email_institucional)
        worksheet.write(row, 3, pp.get_cargo_display())
        worksheet.write(row, 4, str(pp.colegio))
        worksheet.write(row, 5, str(pp.fundacion))
        worksheet.write(row, 6, pp.rut)
        worksheet.write(row, 7, pp.nombre)
        worksheet.write(row, 8, pp.persona.email_institucional)
        worksheet.write(row, 9, pp.get_cargo_display())
        worksheet.write(row, 10, str(pp.colegio))
        worksheet.write(row, 11, str(pp.fundacion))

        row += 1

    workbook.close()
    output.seek(0)

    # Set up the Http response.
    filename = 'profesores-auto.xlsx'
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response


@login_required
def profesores_pares(request):
    output = io.BytesIO()

    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet('Profesores')
    
    # Some data we want to write to the worksheet.
    qs = get_for_user(request, Profesor.objects.all(), 'colegio__pk', request.user)

    # Start from the first cell. Rows and columns are zero indexed.
    row = 0
    col = 0

    # Iterate over the data and write it out row by row.
    worksheet.write(0, 0, 'RUT Evaluador')
    worksheet.write(0, 1, 'Nombres Evaluador')
    worksheet.write(0, 2, 'Correo Institucional Evaluador')
    worksheet.write(0, 3, 'Función Evaluador')
    worksheet.write(0, 4, 'Colegio Evaluador')
    worksheet.write(0, 5, 'Fundación Evaluador')
    worksheet.write(0, 6, 'RUT Evaluado')
    worksheet.write(0, 7, 'Nombres Evaluado')
    worksheet.write(0, 8, 'Correo Institucional Evaluado')
    worksheet.write(0, 9, 'Función Evaluado')
    worksheet.write(0, 10, 'Colegio Evaluado')
    worksheet.write(0, 11, 'Fundación Evaluado')


    row = 1

    workbook.close()
    output.seek(0)

    # Set up the Http response.
    filename = 'profesores-pares.xlsx'
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response


@login_required
def profesores_directivos(request):
    output = io.BytesIO()

    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet('Profesores')

    # Some data we want to write to the worksheet.
    
    # Profesor.objects.filter(
    #     Q(cargo="3") | Q(cargo="5") | Q(cargo="6") | Q(cargo="7") | Q(cargo="9")
    # )

    qs = get_for_user(request, Profesor.objects.all(), 'colegio__pk', request.user)


    # Start from the first cell. Rows and columns are zero indexed.
    row = 0
    col = 0

    # Iterate over the data and write it out row by row.
    worksheet.write(0, 0, 'RUT Evaluador')
    worksheet.write(0, 1, 'Nombres Evaluador')
    worksheet.write(0, 2, 'Correo Institucional Evaluador')
    worksheet.write(0, 3, 'Función Evaluador')
    worksheet.write(0, 4, 'Colegio Evaluador')
    worksheet.write(0, 5, 'Fundación Evaluador')
    worksheet.write(0, 6, 'RUT Evaluado')
    worksheet.write(0, 7, 'Nombres Evaluado')
    worksheet.write(0, 8, 'Correo Institucional Evaluado')
    worksheet.write(0, 9, 'Función Evaluado')
    worksheet.write(0, 10, 'Colegio Evaluado')
    worksheet.write(0, 11, 'Fundación Evaluado')

    row = 1
    for pp in qs:
        worksheet.write(row, 0, pp.rut)
        worksheet.write(row, 1, pp.nombre)
        worksheet.write(row, 2, pp.persona.email_institucional)
        worksheet.write(row, 3, pp.get_cargo_display())
        worksheet.write(row, 4, str(pp.colegio))
        worksheet.write(row, 5, str(pp.fundacion))
        worksheet.write(row, 6, pp.rut)
        worksheet.write(row, 7, pp.nombre)
        worksheet.write(row, 8, pp.persona.email_institucional)
        worksheet.write(row, 9, pp.get_cargo_display())
        worksheet.write(row, 10, str(pp.colegio))
        worksheet.write(row, 11, str(pp.fundacion))

        row += 1

    workbook.close()
    output.seek(0)

    # Set up the Http response.
    filename = 'profesores-directivos.xlsx'
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response

@login_required
def asistentes_info(request):
    output = io.BytesIO()

    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet('Asistentes')
    
    # Some data we want to write to the worksheet.
    qs = get_for_user(request, Asistente.objects.all(), 'colegio__pk', request.user)

    # Start from the first cell. Rows and columns are zero indexed.
    row = 0
    col = 0

    # Iterate over the data and write it out row by row.
    worksheet.write(0, 0, 'RUT')
    worksheet.write(0, 1, 'Nombre Asistente')
    worksheet.write(0, 2, 'Fecha de Nacimiento')
    worksheet.write(0, 3, 'Nacionalidad')
    worksheet.write(0, 4, 'Dirección')
    worksheet.write(0, 5, 'Comuna')
    worksheet.write(0, 6, 'Teléfono')
    worksheet.write(0, 7, 'Email personal')
    worksheet.write(0, 8, 'Email institucional')
    worksheet.write(0, 9, 'Estado civil')
    worksheet.write(0, 10, 'Adventista')
    worksheet.write(0, 11, 'Discapacidad')
    worksheet.write(0, 12, 'Recibe pensión')
    worksheet.write(0, 13, 'Fecha de Inicio Contrato')
    worksheet.write(0, 14, 'Horas Contrato')
    worksheet.write(0, 15, 'Función')
    worksheet.write(0, 16, 'SEP')
    worksheet.write(0, 17, 'PIE')
    worksheet.write(0, 18, 'Sostenedor')
    worksheet.write(0, 19, 'Fundación que lo contrata')
    worksheet.write(0, 20, 'Colegio')


    row = 1
    for pp in qs:
        worksheet.write(row, 0, pp.rut)
        worksheet.write(row, 1, pp.nombre)
        worksheet.write(row, 2, pp.persona.fecha_nacimiento)
        worksheet.write(row, 3, pp.persona.nacionalidad)
        worksheet.write(row, 4, pp.persona.direccion)
        worksheet.write(row, 5, pp.persona.comuna)
        worksheet.write(row, 6, pp.persona.telefono)
        worksheet.write(row, 7, pp.persona.email_personal)
        worksheet.write(row, 8, pp.persona.email_institucional)
        worksheet.write(row, 9, pp.persona.get_estado_civil_display())
        worksheet.write(row, 10, 'Sí' if pp.persona.adventista else 'No')
        worksheet.write(row, 11, 'Sí' if pp.persona.discapacidad else 'No')
        worksheet.write(row, 12, 'Sí' if pp.persona.recibe_pension else 'No')
        worksheet.write(row, 13, pp.fecha_inicio)
        worksheet.write(row, 14, pp.horas)
        worksheet.write(row, 15, pp.funcion)
        worksheet.write(row, 16, pp.horas_sep)
        worksheet.write(row, 17, pp.horas_pie)
        worksheet.write(row, 18, pp.horas_sostenedor)
        worksheet.write(row, 19, str(pp.fundacion))
        worksheet.write(row, 20, str(pp.colegio))
        row += 1

    workbook.close()
    output.seek(0)

    # Set up the Http response.
    filename = 'asistentes-info.xlsx'
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response

def uploadFile(request):
    if request.method == "POST":
        # Fetching the form data
        fileTitle = request.POST["fileTitle"]
        uploadedFile = request.FILES["uploadedFile"]

        # Saving the information in the database
        document = models.Document(
            title = fileTitle,
            uploadedFile = uploadedFile
        )
        document.save()

    documents = models.Document.objects.all()
    return redirect('carga-horaria:profesores')
    #return render(request, "carga_horaria/profesor/listado_profesor.html", context = {
    #    "files": documents
    #})