from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.core.urlresolvers import reverse_lazy
from rrhh.models.base import Perfil, Banco, AFP, Isapre, Funcion, TipoLicencia, TipoDocumento, TipoTitulo, AreaTitulo
from rrhh.models.base import Especialidad, Mencion
from rrhh.models.union import Union
from rrhh.models.fundacion import Fundacion
from rrhh.models.colegio import Colegio
from gestion.forms import UnionForm, FundacionForm, ColegioForm, UserForm, UserUpdateForm, PerfilForm, BancoForm
from gestion.forms import AFPForm, IsapreForm, FuncionForm, TipoLicenciaForm, TipoDocumentoForm, TipoTituloForm
from gestion.forms import AreaTituloForm, EspecialidadForm, MencionForm


class UnionListView(LoginRequiredMixin, ListView):
    model = Union
    template_name = 'gestion/union/listado_union.html'
    paginate_by = 10


class UnionCreateView(LoginRequiredMixin, CreateView):
    model = Union
    form_class = UnionForm
    template_name = 'gestion/union/nuevo_union.html'

    def get_success_url(self):
        return reverse_lazy(
            'rrgestionhh:union',
            kwargs={
                'pk': self.object.pk,
            }
        )


class UnionDetailView(LoginRequiredMixin, DetailView):
    model = Union
    template_name = 'gestion/union/detalle_union.html'


class UnionUpdateView(LoginRequiredMixin, UpdateView):
    model = Union
    form_class = UnionForm
    template_name = 'gestion/union/nuevo_union.html'

    def get_success_url(self):
        return reverse_lazy(
            'gestion:union',
            kwargs={
                'pk': self.object.pk,
            }
        )


class UnionDeleteView(LoginRequiredMixin, DeleteView):
    model = Union
    success_url = reverse_lazy('gestion:uniones')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class FundacionListView(LoginRequiredMixin, ListView):
    model = Fundacion
    template_name = 'gestion/fundacion/listado_fundacion.html'
    paginate_by = 10


class FundacionCreateView(LoginRequiredMixin, CreateView):
    model = Fundacion
    form_class = FundacionForm
    template_name = 'gestion/fundacion/nuevo_fundacion.html'

    def get_success_url(self):
        return reverse_lazy(
            'gestion:fundacion',
            kwargs={
                'pk': self.object.pk,
            }
        )


class FundacionDetailView(LoginRequiredMixin, DetailView):
    model = Fundacion
    template_name = 'gestion/fundacion/detalle_fundacion.html'


class FundacionUpdateView(LoginRequiredMixin, UpdateView):
    model = Fundacion
    form_class = FundacionForm
    template_name = 'gestion/fundacion/nuevo_fundacion.html'

    def get_success_url(self):
        return reverse_lazy(
            'gestion:fundacion',
            kwargs={
                'pk': self.object.pk,
            }
        )


class FundacionDeleteView(LoginRequiredMixin, DeleteView):
    model = Fundacion
    success_url = reverse_lazy('gestion:fundaciones')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class ColegioListView(LoginRequiredMixin, ListView):
    model = Colegio
    template_name = 'gestion/colegio/listado_colegio.html'
    paginate_by = 10


class ColegioCreateView(LoginRequiredMixin, CreateView):
    model = Colegio
    form_class = ColegioForm
    template_name = 'gestion/colegio/nuevo_colegio.html'

    def get_success_url(self):
        return reverse_lazy(
            'gestion:colegio',
            kwargs={
                'pk': self.object.pk,
            }
        )


class ColegioDetailView(LoginRequiredMixin, DetailView):
    model = Colegio
    template_name = 'gestion/colegio/detalle_colegio.html'


class ColegioUpdateView(LoginRequiredMixin, UpdateView):
    model = Colegio
    form_class = ColegioForm
    template_name = 'gestion/colegio/nuevo_colegio.html'

    def get_success_url(self):
        return reverse_lazy(
            'gestion:colegio',
            kwargs={
                'pk': self.object.pk,
            }
        )


class ColegioDeleteView(LoginRequiredMixin, DeleteView):
    model = Colegio
    success_url = reverse_lazy('gestion:colegios')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'gestion/usuario/listado_usuario.html'
    search_fields = ['username', 'first_name', 'last_name', 'email']
    paginate_by = 6


@login_required()
def crear_usuario(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            # redirect, or however you want to get to the main view
            return redirect('gestion:usuarios')
    else:
        form = UserForm()

    return render(request, 'gestion/usuario/nuevo_usuario.html', {'form': form})


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """
        Permite la edición de un usuario.
    """
    model = User
    form_class = UserUpdateForm
    template_name = 'gestion/usuario/nuevo_usuario.html'
    success_message = u"Usuario %(username)s actualizado satisfactoriamente."
    success_url = reverse_lazy('gestion:usuarios')
    error_message = "Revise que todos los campos del formulario hayan sido validados correctamente."


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('gestion:usuarios')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


@login_required()
def change_password(request, id_usuario):
    usuario = get_object_or_404(
        User,
        id=id_usuario
    )

    context = {
        'usuario': usuario
    }

    if request.method == 'POST':
        password1 = request.POST.get('password1', None)
        password2 = request.POST.get('password2', None)

        if password1 == password2:
            usuario.set_password(password1)
            usuario.save()
            messages.success(request, u'La contraseña fue actualizada con exito!')
            return redirect('gestion:usuarios')
        else:
            messages.error(
                request,
                u"Estimado/a %s, no fue posible validar su contraseña, "
                u"intentelo nuevamente..." % usuario.get_full_name()
            )

    return render(
        request,
        'gestion/usuario/change_password.html',
        context
    )


class PerfilListView(LoginRequiredMixin, ListView):
    model = Perfil
    template_name = 'gestion/perfil/listado_perfil.html'
    search_fields = ['nombre']
    paginate_by = 10


class PerfilDetailView(LoginRequiredMixin, DetailView):
    model = Perfil
    template_name = 'gestion/perfil/detalle_perfil.html'


class PerfilCreateView(LoginRequiredMixin, CreateView):
    model = Perfil
    form_class = PerfilForm
    template_name = 'gestion/perfil/nuevo_perfil.html'

    def get_success_url(self):
        return reverse_lazy(
            'gestion:perfil',
            kwargs={
                'pk': self.object.pk,
            }
        )


class PerfilUpdateView(LoginRequiredMixin, UpdateView):
    model = Perfil
    form_class = PerfilForm
    template_name = 'gestion/perfil/nuevo_perfil.html'

    def get_success_url(self):
        return reverse_lazy(
            'gestion:perfil',
            kwargs={
                'pk': self.object.pk,
            }
        )


class PerfilDeleteView(LoginRequiredMixin, DeleteView):
    model = Perfil
    success_url = reverse_lazy('gestion:perfiles')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class BancoListView(LoginRequiredMixin, ListView):
    model = Banco
    template_name = 'gestion/banco/listado_banco.html'
    search_fields = ['nombre']
    paginate_by = 10


class BancoDetailView(LoginRequiredMixin, DetailView):
    model = Banco
    template_name = 'gestion/banco/detalle_banco.html'


class BancoCreateView(LoginRequiredMixin, CreateView):
    model = Banco
    form_class = BancoForm
    template_name = 'gestion/banco/nuevo_banco.html'

    def get_success_url(self):
        return reverse_lazy(
            'gestion:banco',
            kwargs={
                'pk': self.object.pk,
            }
        )


class BancoUpdateView(LoginRequiredMixin, UpdateView):
    model = Banco
    form_class = BancoForm
    template_name = 'gestion/banco/nuevo_banco.html'

    def get_success_url(self):
        return reverse_lazy(
            'gestion:banco',
            kwargs={
                'pk': self.object.pk,
            }
        )


class BancoDeleteView(LoginRequiredMixin, DeleteView):
    model = Banco
    success_url = reverse_lazy('gestion:bancos')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class AFPListView(LoginRequiredMixin, ListView):
    model = AFP
    template_name = 'gestion/afp/listado_afp.html'
    search_fields = ['nombre']
    paginate_by = 10


class AFPDetailView(LoginRequiredMixin, DetailView):
    model = AFP
    template_name = 'gestion/afp/detalle_afp.html'


class AFPCreateView(LoginRequiredMixin, CreateView):
    model = AFP
    form_class = AFPForm
    template_name = 'gestion/afp/nueva_afp.html'

    def get_success_url(self):
        return reverse_lazy(
            'gestion:afp',
            kwargs={
                'pk': self.object.pk,
            }
        )


class AFPUpdateView(LoginRequiredMixin, UpdateView):
    model = AFP
    form_class = AFPForm
    template_name = 'gestion/afp/nueva_afp.html'

    def get_success_url(self):
        return reverse_lazy(
            'gestion:afp',
            kwargs={
                'pk': self.object.pk,
            }
        )


class AFPDeleteView(LoginRequiredMixin, DeleteView):
    model = AFP
    success_url = reverse_lazy('gestion:afps')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class IsapreListView(LoginRequiredMixin, ListView):
    model = Isapre
    template_name = 'gestion/isapre/listado_isapre.html'
    search_fields = ['nombre']
    paginate_by = 10


class IsapreDetailView(LoginRequiredMixin, DetailView):
    model = Isapre
    template_name = 'gestion/isapre/detalle_isapre.html'


class IsapreCreateView(LoginRequiredMixin, CreateView):
    model = Isapre
    form_class = IsapreForm
    template_name = 'gestion/isapre/nueva_isapre.html'

    def get_success_url(self):
        return reverse_lazy(
            'gestion:isapre',
            kwargs={
                'pk': self.object.pk,
            }
        )


class IsapreUpdateView(LoginRequiredMixin, UpdateView):
    model = Isapre
    form_class = IsapreForm
    template_name = 'gestion/isapre/nueva_isapre.html'

    def get_success_url(self):
        return reverse_lazy(
            'gestion:isapre',
            kwargs={
                'pk': self.object.pk,
            }
        )


class IsapreDeleteView(LoginRequiredMixin, DeleteView):
    model = Isapre
    success_url = reverse_lazy('gestion:isapres')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class FuncionListView(LoginRequiredMixin, ListView):
    model = Funcion
    template_name = 'gestion/funcion/listado_funcion.html'
    search_fields = ['nombre']
    paginate_by = 10


class FuncionDetailView(LoginRequiredMixin, DetailView):
    model = Funcion
    template_name = 'gestion/funcion/detalle_funcion.html'


class FuncionCreateView(LoginRequiredMixin, CreateView):
    model = Funcion
    form_class = FuncionForm
    template_name = 'gestion/funcion/nueva_funcion.html'

    def get_success_url(self):
        return reverse_lazy(
            'gestion:funcion',
            kwargs={
                'pk': self.object.pk,
            }
        )


class FuncionUpdateView(LoginRequiredMixin, UpdateView):
    model = Funcion
    form_class = FuncionForm
    template_name = 'gestion/funcion/nueva_funcion.html'

    def get_success_url(self):
        return reverse_lazy(
            'gestion:funcion',
            kwargs={
                'pk': self.object.pk,
            }
        )


class FuncionDeleteView(LoginRequiredMixin, DeleteView):
    model = Funcion
    success_url = reverse_lazy('gestion:funciones')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class TipoLicenciaListView(LoginRequiredMixin, ListView):
    model = TipoLicencia
    template_name = 'gestion/tipo_licencia/listado_tipolicencia.html'
    search_fields = ['nombre']
    paginate_by = 10


class TipoLicenciaDetailView(LoginRequiredMixin, DetailView):
    model = TipoLicencia
    template_name = 'gestion/tipo_licencia/detalle_tipolicencia.html'


class TipoLicenciaCreateView(LoginRequiredMixin, CreateView):
    model = TipoLicencia
    form_class = TipoLicenciaForm
    template_name = 'gestion/tipo_licencia/nuevo_tipolicencia.html'

    def get_success_url(self):
        return reverse_lazy(
            'gestion:tipolicencia',
            kwargs={
                'pk': self.object.pk,
            }
        )


class TipoLicenciaUpdateView(LoginRequiredMixin, UpdateView):
    model = TipoLicencia
    form_class = TipoLicenciaForm
    template_name = 'gestion/tipo_licencia/nuevo_tipolicencia.html'

    def get_success_url(self):
        return reverse_lazy(
            'gestion:tipolicencia',
            kwargs={
                'pk': self.object.pk,
            }
        )


class TipoLicenciaDeleteView(LoginRequiredMixin, DeleteView):
    model = TipoLicencia
    success_url = reverse_lazy('gestion:tiposlicencia')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class TipoDocumentoListView(LoginRequiredMixin, ListView):
    model = TipoDocumento
    template_name = 'gestion/tipo_documento/listado_tipodocumento.html'
    search_fields = ['nombre']
    paginate_by = 10


class TipoDocumentoDetailView(LoginRequiredMixin, DetailView):
    model = TipoDocumento
    template_name = 'gestion/tipo_documento/detalle_tipodocumento.html'


class TipoDocumentoCreateView(LoginRequiredMixin, CreateView):
    model = TipoDocumento
    form_class = TipoDocumentoForm
    template_name = 'gestion/tipo_documento/nuevo_tipodocumento.html'

    def get_success_url(self):
        return reverse_lazy(
            'gestion:tipodocumento',
            kwargs={
                'pk': self.object.pk,
            }
        )


class TipoDocumentoUpdateView(LoginRequiredMixin, UpdateView):
    model = TipoDocumento
    form_class = TipoDocumentoForm
    template_name = 'gestion/tipo_documento/nuevo_tipodocumento.html'

    def get_success_url(self):
        return reverse_lazy(
            'gestion:tipodocumento',
            kwargs={
                'pk': self.object.pk,
            }
        )


class TipoDocumentoDeleteView(LoginRequiredMixin, DeleteView):
    model = TipoDocumento
    success_url = reverse_lazy('gestion:tiposdocumento')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class TipoTituloListView(LoginRequiredMixin, ListView):
    model = TipoTitulo
    template_name = 'gestion/tipo_titulo/listado_tipotitulo.html'
    search_fields = ['nombre']
    paginate_by = 10


class TipoTituloDetailView(LoginRequiredMixin, DetailView):
    model = TipoTitulo
    template_name = 'gestion/tipo_titulo/detalle_tipotitulo.html'


class TipoTituloCreateView(LoginRequiredMixin, CreateView):
    model = TipoTitulo
    form_class = TipoTituloForm
    template_name = 'gestion/tipo_titulo/nuevo_tipotitulo.html'

    def get_success_url(self):
        return reverse_lazy(
            'gestion:tipotitulo',
            kwargs={
                'pk': self.object.pk,
            }
        )


class TipoTituloUpdateView(LoginRequiredMixin, UpdateView):
    model = TipoTitulo
    form_class = TipoTituloForm
    template_name = 'gestion/tipo_titulo/nuevo_tipotitulo.html'

    def get_success_url(self):
        return reverse_lazy(
            'gestion:tipotitulo',
            kwargs={
                'pk': self.object.pk,
            }
        )


class TipoTituloDeleteView(LoginRequiredMixin, DeleteView):
    model = TipoTitulo
    success_url = reverse_lazy('gestion:tipostitulo')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class AreaTituloListView(LoginRequiredMixin, ListView):
    model = AreaTitulo
    template_name = 'gestion/area_titulo/listado_areatitulo.html'
    search_fields = ['nombre']
    paginate_by = 10


class AreaTituloDetailView(LoginRequiredMixin, DetailView):
    model = AreaTitulo
    template_name = 'gestion/area_titulo/detalle_areatitulo.html'


class AreaTituloCreateView(LoginRequiredMixin, CreateView):
    model = AreaTitulo
    form_class = AreaTituloForm
    template_name = 'gestion/area_titulo/nuevo_areatitulo.html'

    def get_success_url(self):
        return reverse_lazy(
            'gestion:areatitulo',
            kwargs={
                'pk': self.object.pk,
            }
        )


class AreaTituloUpdateView(LoginRequiredMixin, UpdateView):
    model = AreaTitulo
    form_class = AreaTituloForm
    template_name = 'gestion/area_titulo/nuevo_areatitulo.html'

    def get_success_url(self):
        return reverse_lazy(
            'gestion:areatitulo',
            kwargs={
                'pk': self.object.pk,
            }
        )


class AreaTituloDeleteView(LoginRequiredMixin, DeleteView):
    model = AreaTitulo
    success_url = reverse_lazy('gestion:areastitulo')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class EspecialidadListView(LoginRequiredMixin, ListView):
    model = Especialidad
    template_name = 'gestion/especialidad/listado_especialidad.html'
    search_fields = ['nombre']
    paginate_by = 10


class EspecialidadDetailView(LoginRequiredMixin, DetailView):
    model = Especialidad
    template_name = 'gestion/especialidad/detalle_especialidad.html'


class EspecialidadCreateView(LoginRequiredMixin, CreateView):
    model = Especialidad
    form_class = EspecialidadForm
    template_name = 'gestion/especialidad/nuevo_especialidad.html'

    def get_success_url(self):
        return reverse_lazy(
            'gestion:especialidad',
            kwargs={
                'pk': self.object.pk,
            }
        )


class EspecialidadUpdateView(LoginRequiredMixin, UpdateView):
    model = Especialidad
    form_class = EspecialidadForm
    template_name = 'gestion/especialidad/nuevo_especialidad.html'

    def get_success_url(self):
        return reverse_lazy(
            'gestion:especialidad',
            kwargs={
                'pk': self.object.pk,
            }
        )


class EspecialidadDeleteView(LoginRequiredMixin, DeleteView):
    model = Especialidad
    success_url = reverse_lazy('gestion:especialidades')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class MencionListView(LoginRequiredMixin, ListView):
    model = Mencion
    template_name = 'gestion/mencion/listado_mencion.html'
    search_fields = ['nombre']
    paginate_by = 10


class MencionDetailView(LoginRequiredMixin, DetailView):
    model = Mencion
    template_name = 'gestion/mencion/detalle_mencion.html'


class MencionCreateView(LoginRequiredMixin, CreateView):
    model = Mencion
    form_class = MencionForm
    template_name = 'gestion/mencion/nuevo_mencion.html'

    def get_success_url(self):
        return reverse_lazy(
            'gestion:mencion',
            kwargs={
                'pk': self.object.pk,
            }
        )


class MencionUpdateView(LoginRequiredMixin, UpdateView):
    model = Mencion
    form_class = MencionForm
    template_name = 'gestion/mencion/nuevo_mencion.html'

    def get_success_url(self):
        return reverse_lazy(
            'gestion:mencion',
            kwargs={
                'pk': self.object.pk,
            }
        )


class MencionDeleteView(LoginRequiredMixin, DeleteView):
    model = Mencion
    success_url = reverse_lazy('gestion:menciones')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
