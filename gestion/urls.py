from django.conf import settings
from django.conf.urls import url
from gestion import views

app_name = 'gestion'

urlpatterns = [
    url(
        r'^entidades/$',
        views.EntidadListView.as_view(),
        name='entidades'
    ),
    url(
        r'^entidades/nuevo/$',
        views.EntidadCreateView.as_view(),
        name='entidad__nuevo'
    ),
    url(
        r'^entidades/(?P<pk>\d+)/$',
        views.EntidadDetailView.as_view(),
        name='entidad'
    ),
    url(
        r'^entidades/(?P<pk>\d+)/editar/$',
        views.EntidadUpdateView.as_view(),
        name='entidad__editar'
    ),
    url(
        r'^entidades/(?P<pk>\d+)/eliminar/$',
        views.EntidadDeleteView.as_view(),
        name='entidad__eliminar'
    ),
    url(
        r'^usuarios/nuevo/$',
        views.crear_usuario,
        name='usuario__nuevo'
    ),
    url(
        r'^usuarios/$',
        views.UserListView.as_view(),
        name='usuarios'
    ),
    url(
        r'^usuarios/(?P<pk>\d+)/editar/$',
        views.UserUpdateView.as_view(),
        name='usuario__editar'
    ),
    url(
        r'^usuarios/(?P<pk>\d+)/eliminar/$',
        views.UserDeleteView.as_view(),
        name='usuario__eliminar'
    ),
    url(
        r'^change_password/(?P<id_usuario>\d+)/$',
        views.change_password,
        name='change_password'
    ),
    url(
        r'^cambiar_perfil_usuario/(?P<id_usuario>\d+)/$',
        views.cambiar_perfil_usuario,
        name='cambiar_perfil_usuario'
    ),
    url(
        r'^perfiles/$',
        views.PerfilListView.as_view(),
        name='perfiles'
    ),
    url(
        r'^perfiles/nuevo/$',
        views.PerfilCreateView.as_view(),
        name='perfil__nuevo'
    ),
    url(
        r'^perfiles/(?P<pk>\d+)/$',
        views.PerfilDetailView.as_view(),
        name='perfil'
    ),
    url(
        r'^perfiles/(?P<pk>\d+)/editar/$',
        views.PerfilUpdateView.as_view(),
        name='perfil__editar'
    ),
    url(
        r'^perfiles/(?P<pk>\d+)/eliminar/$',
        views.PerfilDeleteView.as_view(),
        name='perfil__eliminar'
    ),
    url(
        r'^bancos/$',
        views.BancoListView.as_view(),
        name='bancos'
    ),
    url(
        r'^bancos/nuevo/$',
        views.BancoCreateView.as_view(),
        name='banco__nuevo'
    ),
    url(
        r'^bancos/(?P<pk>\d+)/$',
        views.BancoDetailView.as_view(),
        name='banco'
    ),
    url(
        r'^bancos/(?P<pk>\d+)/editar/$',
        views.BancoUpdateView.as_view(),
        name='banco__editar'
    ),
    url(
        r'^bancos/(?P<pk>\d+)/eliminar/$',
        views.BancoDeleteView.as_view(),
        name='banco__eliminar'
    ),
    url(
        r'^afps/$',
        views.AFPListView.as_view(),
        name='afps'
    ),
    url(
        r'^afps/nuevo/$',
        views.AFPCreateView.as_view(),
        name='afp__nuevo'
    ),
    url(
        r'^afps/(?P<pk>\d+)/$',
        views.AFPDetailView.as_view(),
        name='afp'
    ),
    url(
        r'^afps/(?P<pk>\d+)/editar/$',
        views.AFPUpdateView.as_view(),
        name='afp__editar'
    ),
    url(
        r'^afps/(?P<pk>\d+)/eliminar/$',
        views.AFPDeleteView.as_view(),
        name='afp__eliminar'
    ),
    url(
        r'^isapres/$',
        views.IsapreListView.as_view(),
        name='isapres'
    ),
    url(
        r'^isapres/nuevo/$',
        views.IsapreCreateView.as_view(),
        name='isapre__nuevo'
    ),
    url(
        r'^isapres/(?P<pk>\d+)/$',
        views.IsapreDetailView.as_view(),
        name='isapre'
    ),
    url(
        r'^isapres/(?P<pk>\d+)/editar/$',
        views.IsapreUpdateView.as_view(),
        name='isapre__editar'
    ),
    url(
        r'^isapres/(?P<pk>\d+)/eliminar/$',
        views.IsapreDeleteView.as_view(),
        name='isapre__eliminar'
    ),
    url(
        r'^funciones/$',
        views.FuncionListView.as_view(),
        name='funciones'
    ),
    url(
        r'^funciones/nuevo/$',
        views.FuncionCreateView.as_view(),
        name='funcion__nuevo'
    ),
    url(
        r'^funciones/(?P<pk>\d+)/$',
        views.FuncionDetailView.as_view(),
        name='funcion'
    ),
    url(
        r'^funciones/(?P<pk>\d+)/editar/$',
        views.FuncionUpdateView.as_view(),
        name='funcion__editar'
    ),
    url(
        r'^funciones/(?P<pk>\d+)/eliminar/$',
        views.FuncionDeleteView.as_view(),
        name='funcion__eliminar'
    ),
    url(
        r'^tiposlicencia/$',
        views.TipoLicenciaListView.as_view(),
        name='tiposlicencia'
    ),
    url(
        r'^tiposlicencia/nuevo/$',
        views.TipoLicenciaCreateView.as_view(),
        name='tipolicencia__nuevo'
    ),
    url(
        r'^tiposlicencia/(?P<pk>\d+)/$',
        views.TipoLicenciaDetailView.as_view(),
        name='tipolicencia'
    ),
    url(
        r'^tiposlicencia/(?P<pk>\d+)/editar/$',
        views.TipoLicenciaUpdateView.as_view(),
        name='tipolicencia__editar'
    ),
    url(
        r'^tiposlicencia/(?P<pk>\d+)/eliminar/$',
        views.TipoLicenciaDeleteView.as_view(),
        name='tipolicencia__eliminar'
    ),
    url(
        r'^tiposdocumento/$',
        views.TipoDocumentoListView.as_view(),
        name='tiposdocumento'
    ),
    url(
        r'^tiposdocumento/nuevo/$',
        views.TipoDocumentoCreateView.as_view(),
        name='tipodocumento__nuevo'
    ),
    url(
        r'^tiposdocumento/(?P<pk>\d+)/$',
        views.TipoDocumentoDetailView.as_view(),
        name='tipodocumento'
    ),
    url(
        r'^tiposdocumento/(?P<pk>\d+)/editar/$',
        views.TipoDocumentoUpdateView.as_view(),
        name='tipodocumento__editar'
    ),
    url(
        r'^tiposdocumento/(?P<pk>\d+)/eliminar/$',
        views.TipoDocumentoDeleteView.as_view(),
        name='tipodocumento__eliminar'
    ),
    url(
        r'^tipostitulo/$',
        views.TipoTituloListView.as_view(),
        name='tipostitulo'
    ),
    url(
        r'^tipostitulo/nuevo/$',
        views.TipoTituloCreateView.as_view(),
        name='tipotitulo__nuevo'
    ),
    url(
        r'^tipostitulo/(?P<pk>\d+)/$',
        views.TipoTituloDetailView.as_view(),
        name='tipotitulo'
    ),
    url(
        r'^tipostitulo/(?P<pk>\d+)/editar/$',
        views.TipoTituloUpdateView.as_view(),
        name='tipotitulo__editar'
    ),
    url(
        r'^tipostitulo/(?P<pk>\d+)/eliminar/$',
        views.TipoTituloDeleteView.as_view(),
        name='tipotitulo__eliminar'
    ),
    url(
        r'^areastitulo/$',
        views.AreaTituloListView.as_view(),
        name='areastitulo'
    ),
    url(
        r'^areastitulo/nuevo/$',
        views.AreaTituloCreateView.as_view(),
        name='areatitulo__nuevo'
    ),
    url(
        r'^areastitulo/(?P<pk>\d+)/$',
        views.AreaTituloDetailView.as_view(),
        name='areatitulo'
    ),
    url(
        r'^areastitulo/(?P<pk>\d+)/editar/$',
        views.AreaTituloUpdateView.as_view(),
        name='areatitulo__editar'
    ),
    url(
        r'^areastitulo/(?P<pk>\d+)/eliminar/$',
        views.AreaTituloDeleteView.as_view(),
        name='areatitulo__eliminar'
    ),
    url(
        r'^especialidades/$',
        views.EspecialidadListView.as_view(),
        name='especialidades'
    ),
    url(
        r'^especialidades/nuevo/$',
        views.EspecialidadCreateView.as_view(),
        name='especialidad__nuevo'
    ),
    url(
        r'^especialidades/(?P<pk>\d+)/$',
        views.EspecialidadDetailView.as_view(),
        name='especialidad'
    ),
    url(
        r'^especialidades/(?P<pk>\d+)/editar/$',
        views.EspecialidadUpdateView.as_view(),
        name='especialidad__editar'
    ),
    url(
        r'^especialidades/(?P<pk>\d+)/eliminar/$',
        views.EspecialidadDeleteView.as_view(),
        name='especialidad__eliminar'
    ),
    url(
        r'^menciones/$',
        views.MencionListView.as_view(),
        name='menciones'
    ),
    url(
        r'^menciones/nuevo/$',
        views.MencionCreateView.as_view(),
        name='mencion__nuevo'
    ),
    url(
        r'^menciones/(?P<pk>\d+)/$',
        views.MencionDetailView.as_view(),
        name='mencion'
    ),
    url(
        r'^menciones/(?P<pk>\d+)/editar/$',
        views.MencionUpdateView.as_view(),
        name='mencion__editar'
    ),
    url(
        r'^menciones/(?P<pk>\d+)/eliminar/$',
        views.MencionDeleteView.as_view(),
        name='mencion__eliminar'
    ),

]
