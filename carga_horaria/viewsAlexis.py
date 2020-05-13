from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from carga_horaria.models import Profesor, AsignaturaBase, Asignatura
from carga_horaria.formsAlexis import ProfesorForm, AsignaturaBaseForm, AsignaturaCreateForm, AsignaturaUpdateForm
from django.core.urlresolvers import reverse_lazy, reverse
from .models import Periodo
from .models import Nivel


class LevelFilterMixin(object):
    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx['levels'] = [(tag.name, tag.value) for tag in Nivel][::-1]
        ctx['nivel_actual'] = self.request.GET.get('nivel')
        return ctx

    def get_queryset(self):
        qs = super().get_queryset()

        nivel = self.request.GET.get('nivel')
        if nivel:
            qs = qs.filter(plan__nivel=nivel)

        return qs


"""
    Comienzo Crud Profesor
"""
class ProfesorListView(ListView):
    """
        Listado de profesores
    """
    model = Profesor
    template_name = 'carga_horaria/profesor/listado_profesor.html'
    search_fields = ['nombre', 'horas']
    paginate_by = 6


class ProfesorDetailView(DetailView):
    """
        Detalle de Profesor
    """
    model = Profesor
    template_name = 'carga_horaria/profesor/detalle_profesor.html'


class ProfesorCreateView(CreateView):
    model = Profesor
    form_class = ProfesorForm
    template_name = 'carga_horaria/profesor/nuevo_profesor.html'
    success_url = reverse_lazy('carga-horaria:profesores')


class ProfesorUpdateView(UpdateView):
    model = Profesor
    form_class = ProfesorForm
    template_name = 'carga_horaria/profesor/editar_profesor.html'

    def get_success_url(self):
        return reverse(
            'carga-horaria:profesor',
            kwargs={
                'pk': self.object.pk,
            }
        )


class ProfesorDeleteView(DeleteView):
    model = Profesor
    success_url = reverse_lazy('carga-horaria:profesores')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


# """
#     Comienzo Crud Curso
# """
# class CursoListView(ListView):
#     """
#         Listado de cursos
#     """
#     model = Curso
#     template_name = 'carga_horaria/curso/listado_curso.html'
#     search_fields = ['periodo', 'letra']
#     paginate_by = 6


# class CursoDetailView(DetailView):
#     """
#         Detalle de curso
#     """
#     model = Curso
#     template_name = 'carga_horaria/curso/detalle_curso.html'


# class CursoCreateView(CreateView):
#     model = Curso
#     form_class = CursoForm
#     template_name = 'carga_horaria/curso/nuevo_curso.html'
#     success_url = reverse_lazy('carga-horaria:cursos')


# class CursoUpdateView(UpdateView):
#     model = Curso
#     form_class = CursoForm
#     template_name = 'carga_horaria/curso/editar_curso.html'

#     def get_success_url(self):
#         return reverse(
#             'carga-horaria:curso',
#             kwargs={
#                 'pk': self.object.pk,
#             }
#         )


# class CursoDeleteView(DeleteView):
#     model = Curso
#     success_url = reverse_lazy('carga-horaria:cursos')

#     def get(self, request, *args, **kwargs):
#         return self.post(request, *args, **kwargs)


"""
    Comienzo Crud Asignatura Base
"""
class AsignaturaBaseListView(ListView):
    """
        Listado de asignatura base
    """
    model = AsignaturaBase
    template_name = 'carga_horaria/asignaturabase/listado_asignaturabase.html'
    search_fields = ['nombre', 'plan']
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx['levels'] = [(tag.name, tag.value) for tag in Nivel]
        ctx['nivel_actual'] = self.request.GET.get('nivel')
        return ctx

    def get_queryset(self):
        qs = super().get_queryset()

        nivel = self.request.GET.get('nivel')
        if nivel:
            qs = qs.filter(plan__nivel=nivel)

        return qs


class AsignaturaBaseDetailView(DetailView):
    """
        Detalle de asignatura base
    """
    model = AsignaturaBase
    template_name = 'carga_horaria/asignaturabase/detalle_asignaturabase.html'


class AsignaturaBaseCreateView(CreateView):
    model = AsignaturaBase
    form_class = AsignaturaBaseForm
    template_name = 'carga_horaria/asignaturabase/nuevo_asignaturabase.html'
    success_url = reverse_lazy('carga-horaria:asignaturasbase')


class AsignaturaBaseUpdateView(UpdateView):
    model = AsignaturaBase
    form_class = AsignaturaBaseForm
    template_name = 'carga_horaria/asignaturabase/editar_asignaturabase.html'

    def get_success_url(self):
        return reverse(
            'carga-horaria:asignaturabase',
            kwargs={
                'pk': self.object.pk,
            }
        )


class AsignaturaBaseDeleteView(DeleteView):
    model = AsignaturaBase
    success_url = reverse_lazy('carga-horaria:asignaturasbase')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


"""
    Comienzo Crud Asignatura
"""
class AsignaturaListView(ListView):
    """
        Listado de asignatura
    """
    model = Asignatura
    template_name = 'carga_horaria/asignatura/listado_asignatura.html'
    search_fields = ['base', 'periodo']
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx['levels'] = [(tag.name, tag.value) for tag in Nivel][::-1]
        ctx['nivel_actual'] = self.request.GET.get('nivel')
        return ctx

    def get_queryset(self):
        qs = super().get_queryset()

        nivel = self.request.GET.get('nivel')
        if nivel:
            qs = qs.filter(base__plan__nivel=nivel)

        periodo = self.request.GET.get('periodo')
        if periodo:
            qs = qs.filter(periodo__pk=periodo)
        return qs


class AsignaturaDetailView(DetailView):
    """
        Detalle de asignatura
    """
    model = Asignatura
    template_name = 'carga_horaria/asignatura/detalle_asignatura.html'


class AsignaturaCreateView(CreateView):
    model = Asignatura
    form_class = AsignaturaCreateForm
    template_name = 'carga_horaria/asignatura/nuevo_asignatura.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.periodo = Periodo.objects.get(pk=self.kwargs['pk'])
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse(
            'carga-horaria:periodo',
            kwargs={
                'pk': self.object.periodo.pk,
            }
        )



class AsignaturaUpdateView(UpdateView):
    model = Asignatura
    form_class = AsignaturaUpdateForm
    template_name = 'carga_horaria/asignatura/editar_asignatura.html'

    def get_success_url(self):
        return reverse(
            'carga-horaria:asignatura',
            kwargs={
                'pk': self.object.pk,
            }
        )


class AsignaturaDeleteView(DeleteView):
    model = Asignatura

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse(
            'carga-horaria:periodo',
            kwargs={
                'pk': self.request.GET.get('periodo'),
            }
        )
