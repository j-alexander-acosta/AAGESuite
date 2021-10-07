from django.conf import settings
from django.conf.urls import url
from evado import views

app_name = 'evado'

urlpatterns = [
    url(r'^$', views.home, name='home_evado'),
    # Periodos
    url(r'^periodos/$', views.PeriodoEncuestaListView.as_view(), name='periodo_list'),
    url(r'^periodos/nuevo/$', views.PeriodoEncuestaCreateView.as_view(), name='periodo_create'),
    url(r'^periodos/(?P<pk>\d+)/detalle/$', views.PeriodoEncuestaDetailView.as_view(), name='periodo_detail'),
    url(r'^periodos/(?P<pk>\d+)/actualizar/$', views.PeriodoEncuestaUpdateView.as_view(), name='periodo_update'),
    # Encuestas
    url(r'^encuestas/$', views.EncuestaListView.as_view(), name='encuesta_list'),
    url(r'^encuesta/(?P<pk>\d+)/detalle/$', views.EncuestaDetailView.as_view(), name='encuesta_detail'),
    url(r'^encuesta/nueva/$', views.EncuestaCreateView.as_view(), name='encuesta_create'),
    url(r'^encuesta/(\b[a-f0-9]{128})/$', views.tomar_encuesta, name='tomar_encuesta'),
    url(r'^encuesta/(\b[a-f0-9]{128})/finalizada/$', views.encuesta_finalizada, name='encuesta_finalizada'),
    url(r'^encuesta/(\b[a-f0-9]{128})/cerrada/$', views.encuesta_cerrada, name='encuesta_cerrada'),
    url(r'^encuesta/(?P<id_persona>\d+)/enviar/(?P<id_universo>\d+)/$', views.enviar_encuesta, name='enviar_encuesta'),
    url(r'^encuesta/enviar/(?P<id_universo>\d+)/correos/$', views.enviar_todas_encuestas, name='enviar_todas_encuestas'),
    # Universo Correos
    url(r'^encuesta/correos/$', views.CorreoUniversoEncuestaListView.as_view(), name='correo_universo_list'),
    url(r'^encuesta/correo/<pk>/detalle/$', views.CorreoUniversoEncuestaDetailView.as_view(), name='correo_universo_detail'),
    url(r'^encuesta/correo/nuevo/$', views.CorreoUniversoEncuestaCreateView.as_view(), name='correo_universo_create'),
    url(r'^encuesta/correo/<pk>/actualizar/$', views.CorreoUniversoEncuestaUpdateView.as_view(), name='correo_universo_update'),
    # Categorias
    url(r'^encuestas/preguntas/categorias/$', views.CategoriaPreguntaListView.as_view(), name='categoria_pregunta_list'),
    url(r'^encuestas/preguntas/categoria/(?P<pk>\d+)/actualizar/$', views.CategoriaPreguntaUpdateView.as_view(), name='categoria_pregunta_edit'),
    url(r'^encuestas/preguntas/categoria/nueva/$', views.CategoriaPreguntaCreateView.as_view(), name='categoria_pregunta_create'),
    # Tipos de respuestas
    url(r'^encuestas/tipos_respuestas/$', views.TipoRespuestaListView.as_view(), name='tipo_respuesta_list'),
    url(r'^encuestas/tipos_respuestas/(?P<pk>\d+)/actualizar/$', views.TipoRespuestaUpdateView.as_view(), name='tipo_respuesta_edit'),
    url(r'^encuestas/tipos_respuestas/nueva/$', views.TipoRespuestaCreateView.as_view(), name='tipo_respuesta_create'),
    # Preguntas
    url(r'^encuestas/preguntas/$', views.PreguntaEncuestaListView.as_view(), name='pregunta_encuesta_list'),
    url(r'^encuestas/pregunta/<pk>/$', views.PreguntaEncuestaListView.as_view(), name='pregunta_encuesta_detail'),
    # Tipo Universo Encuesta
    url(r'^tipouniversoencuestas/$', views.TipoUniversoEncuestaListView.as_view(), name='tipo_universo_encuesta_list'),
    url(r'^tipouniversoencuesta/(?P<pk>\d+)/detalle/$', views.TipoUniversoEncuestaDetailView.as_view(), name='tipo_universo_encuesta_detail'),
    url(r'^tipouniversoencuesta/nuevo/$', views.TipoUniversoEncuestaCreateView.as_view(), name='tipo_universo_encuesta_create'),
    url(r'^tipouniversoencuesta/(?P<pk>\d+)/editar/$', views.TipoUniversoEncuestaUpdateView.as_view(), name='tipo_universo_encuesta_edit'),
    url(r'^tipouniversoencuesta/(?P<pk>\d+)/eliminar/$', views.TipoUniversoEncuestaDeleteView.as_view(), name='tipo_universo_encuesta_delete'),
    # Universo Encuestas
    url(r'^universoencuestas/$', views.UniversoEncuestaListView.as_view(), name='universo_encuesta_list'),
    url(r'^universoencuesta/(?P<pk>\d+)/detalle/$', views.UniversoEncuestaDetailView.as_view(), name='universo_encuesta_detail'),
    url(r'^universoencuesta/nuevo/$', views.UniversoEncuestaCreateView.as_view(), name='universo_encuesta_create'),
    url(r'^universoencuesta/(?P<pk>\d+)/editar/$', views.UniversoEncuestaUpdateView.as_view(), name='universo_encuesta_edit'),
    url(r'^universoencuesta/mail/universosencuestas/$', views.enviar_mail_universo_encuestas, name='enviar_mail_universo_encuestas'),
    url(r'^encuesta/(?P<pk>\d+)/editar/$', views.EncuestaPreguntaFormSetView.as_view(), name='encuesta_preguntas_edit'),
    url(r'^encuesta/(?P<pk>\d+)/pregunta/anadir/$', views.encuesta_crear_pregunta, name='encuesta_crear_pregunta'),
    url(r'^encuesta/<pk_pregunta>/pregunta/eliminar/$', views.encuesta_eliminar_pregunta, name='encuesta_eliminar_pregunta'),
    url(r'^universoencuesta/(?P<id_universo>\d+)/actualizar/personas/$', views.actualizar_encuestas_universo, name='actualizar_encuestas_universo'),
    # Correos para enviar
    url(r'^encuesta/correos/<id_universo_correo>/enviar/$', views.enviar_recordar_contestar_encuestas, name='enviar_recordar_contestar_encuestas'),
    # Configurar Universo Encuestas
    url(r'^encuesta/configurar/universo/$', views.configurar_universo_personas, name='configurar_universo_personas'),
    url(r'^encuesta/configurar/(?P<pk>\d+)/eliminar/$', views.eliminar_configurar_universo_personas, name='eliminar_configurar_universo_personas'),
    # url(r'^encuesta/configurar/universo/persona_upload/$', persona_upload, name='persona_upload'),
    url(r'^encuesta/configurar/universo/export/excel/$', views.export_eup_xls, name='export_eup_xls'),
    url(r'^encuesta/configurar/universo/import/excel/$', views.import_eup_xls, name='persona_upload'),
    url(r'^encuesta/configurar/universo/delete/$', views.eliminar_todos_eup, name='eliminar_todos_eup'),
]