from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from django.shortcuts import render, get_object_or_404, redirect
from .viewsAlexis import *
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from carga_horaria.models import Periodo, Colegio, Plan
from carga_horaria.formsDani import PeriodoForm, ColegioForm, PlanForm
from django.core.urlresolvers import reverse_lazy, reverse
from .models import Nivel
from .models import Profesor
from .models import Periodo
from .models import Asignacion
from .models import AsignacionExtra
from .forms import AsignacionForm
from .forms import AsignacionFUAForm
from .forms import AsignacionExtraForm
from .formsDani import PlantillaPlanForm


@login_required
def home(request):
    return render(request, 'carga_horaria/home.html')



@login_required
def anexo(request, pk):
    p = get_object_or_404(Profesor, pk=pk)
    ax = [{'descripcion': 'Planificación', 'curso': '', 'horas': p.horas_planificacion},
          {'descripcion': 'Recreo', 'curso': '', 'horas': p.horas_recreo}] + list(p.asignacionextra_set.all())
    return render(request, 'carga_horaria/profesor/anexo_profesor.html', {'asignaciones': p.asignacion_set.all(),
                                                                          'asignaciones_extra': ax,
                                                                          'profesor': p})


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
    ordering = ['-pk']


class PeriodoDetailView(DetailView):
    """
        Detalle de Periodo
    """
    model = Periodo
    template_name = 'carga_horaria/periodo/detalle_periodo.html'


class PeriodoCreateView(CreateView):
    model = Periodo
    form_class = PeriodoForm
    template_name = 'carga_horaria/periodo/nuevo_periodo.html'
    success_url = reverse_lazy('carga-horaria:periodos')

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(PeriodoCreateView, self).get_form_kwargs(*args, **kwargs)
        kwargs.update({'user': self.request.user})
        return kwargs


class PeriodoUpdateView(UpdateView):
    model = Periodo
    form_class = PeriodoForm
    template_name = 'carga_horaria/periodo/editar_periodo.html'

    def get_success_url(self):
        return reverse(
            'carga-horaria:periodo',
            kwargs={
                'pk': self.object.pk,
            }
        )


class PeriodoDeleteView(LoginRequiredMixin, DeleteView):
    model = Periodo
    success_url = reverse_lazy('carga-horaria:periodos')
    template_name = 'carga_horaria/periodo/eliminar_periodo.html'

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


class ColegioCreateView(CreateView):
    model = Colegio
    form_class = ColegioForm
    template_name = 'carga_horaria/colegio/nuevo_colegio.html'
    success_url = reverse_lazy('carga-horaria:colegios')
#    success_message = u"Nuevo periodo %(nombre)s creado satisfactoriamente."
#    error_message = "Revise que todos los campos del formulario hayan sido validados correctamente."


class ColegioUpdateView(UpdateView):
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
class PlanListView(ListView):
    """
        Listado de planes
    """
    model = Plan
    template_name = 'carga_horaria/plan/listado_planes.html'
    search_fields = ['nombre', 'nivel']
    paginate_by = 10
    ordering = ['-pk']


class PlanDetailView(DetailView):
    """
        Detalle de Plan
    """
    model = Plan
    template_name = 'carga_horaria/plan/detalle_plan.html'


class PlanCreateView(CreateView):
    model = Plan
    form_class = PlanForm
    template_name = 'carga_horaria/plan/nuevo_plan.html'
    success_url = reverse_lazy('carga-horaria:planes')
#    success_message = u"Nuevo periodo %(nombre)s creado satisfactoriamente."
#    error_message = "Revise que todos los campos del formulario hayan sido validados correctamente."


def crear_desde_plantilla(request):
    if request.method == 'POST':
        form = PlantillaPlanForm(request.POST)
        if form.is_valid():
            plantilla = form.cleaned_data['plantilla']
            nivel = form.cleaned_data['nivel']

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


class PlanUpdateView(UpdateView):
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

def asignar(request, pk):
    aa = get_object_or_404(Asignatura, pk=pk)

    if request.method == 'POST':
        form = AsignacionForm(request.POST, asignatura=aa, user=request.user)
        if form.is_valid():
            asignacion = form.save(commit=False)
            asignacion.asignatura = aa
            asignacion.save()
            return redirect('carga-horaria:periodo', aa.periodo.pk)
    else:
        form = AsignacionForm(user=request.user)
    return render(request, 'carga_horaria/asignar.html', {'object': aa,
                                                          'form': form})


def asignar_fua(request, pk, tipo):
    pp = get_object_or_404(Profesor, pk=pk)

    if request.method == 'POST':
        form = AsignacionFUAForm(request.POST, profesor=pp, user=request.user)
        if form.is_valid():
            asignacion = form.save(commit=False)
            asignacion.profesor = pp
            asignacion.tipo = tipo
            asignacion.save()
            return redirect('carga-horaria:profesor', pp.pk)
    else:
        form = AsignacionFUAForm(user=request.user)
    return render(request, 'carga_horaria/asignar_fua.html', {'object': pp,
                                                              'form': form})


def asignar_extra(request, pk):
    pp = get_object_or_404(Profesor, pk=pk)

    if request.method == 'POST':
        form = AsignacionExtraForm(request.POST, profesor=pp, user=request.user)
        if form.is_valid():
            asignacion = form.save(commit=False)
            asignacion.profesor = pp
            asignacion.save()
            return redirect('carga-horaria:profesor', pp.pk)
    else:
        form = AsignacionExtraForm(user=request.user)
    return render(request, 'carga_horaria/asignar_extra.html', {'object': pp,
                                                                'form': form})


class AsignacionDeleteView(LoginRequiredMixin, DeleteView):
    model = Asignacion
    success_url = reverse_lazy('carga-horaria:periodos')
    template_name = 'carga_horaria/periodo/eliminar_periodo.html'

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class AsignacionUpdateView(UpdateView):
    model = Asignacion
    form_class = AsignacionForm
    template_name = 'carga_horaria/asignar.html'

    def get_success_url(self):
        return reverse(
            'carga-horaria:periodo',
            kwargs={
                'pk': self.object.asignatura.periodo.pk,
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
