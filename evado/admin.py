from django.contrib import admin
from nested_inline.admin import NestedStackedInline, NestedTabularInline, NestedModelAdmin
from django_summernote.admin import SummernoteModelAdmin
# from import_export.admin import ImportExportModelAdmin
# from import_export import resources
# from import_export import fields

from evado.models import *


class ItemPersonaUniversoEncuesta(admin.TabularInline):
    model = PersonaUniversoEncuesta
    extra = 1


class ItemRespuestaAplicarUniversoEncuestaPersona(NestedTabularInline):
    model = RespuestaAplicarUniversoEncuestaPersona
    extra = 1
    fk_name = 'aplicar_universo_encuesta_persona'


class ItemAplicarUniversoEncuestaPersona(NestedTabularInline):
    model = AplicarUniversoEncuestaPersona
    extra = 1
    fk_name = 'universo_encuesta'
    inlines = [ItemRespuestaAplicarUniversoEncuestaPersona]


class ItemRespuestaInline(admin.TabularInline):
    model = Respuesta
    extra = 1


class DescripcionItemPreguntaInline(admin.TabularInline):
    model = DescripcionItemPregunta
    extra = 1


class PreguntaEncuestaInline(admin.TabularInline):
    model = PreguntaEncuesta
    extra = 1


# class PersonaUniversoEncuestaResource(resources.ModelResource):
#     class Meta:
#         model = PersonaUniversoEncuesta
#         fields = ('persona__rut', 'persona__nombres', 'persona__apellidos', 'correo_enviado', 'persona__funcion')
#
#
# class AplicarUniversoEncuestaPersonasResource(resources.ModelResource):
#     rut_profesor = fields.Field()
#     nombres_profesor = fields.Field()
#     suma_puntos_profesor = fields.Field()
#
#     class Meta:
#         model = AplicarUniversoEncuestaPersona
#         fields = ('finalizado', 'persona__funcion', 'rut_profesor', 'nombres_profesor',
#                   'universo_encuesta__encuesta__titulo', 'suma_puntos_profesor',
#                   'encuestado')
#
#     def dehydrate_rut_profesor(self, aplicaruniversoencuestapersona):
#         return '%s' % aplicaruniversoencuestapersona.rut_profesor
#
#     def dehydrate_nombres_profesor(self, aplicaruniversoencuestapersona):
#         return '%s' % aplicaruniversoencuestapersona.nombres_profesor
#
#     def dehydrate_suma_puntos_profesor(self, aplicaruniversoencuestapersona):
#         return '%s' % aplicaruniversoencuestapersona.total_respuestas
#
#
# @admin.register(PersonaUniversoEncuesta)
# class PersonaUniversoEncuestaAdmin(ImportExportModelAdmin):
#     resource_class = PersonaUniversoEncuestaResource
#     list_display = ('persona', 'universo_encuesta', 'correo_enviado', 'mail_enviado')
#     list_filter = ['persona__funcion', 'correo_enviado']
#     search_fields = ['persona__nombres', 'persona__apellidos', 'persona__funcion']
#
#
# @admin.register(AplicarUniversoEncuestaPersona)
# class AplicarUniversoEncuestaPersonaAdmin(ImportExportModelAdmin):
#     resource_class = AplicarUniversoEncuestaPersonasResource
#     list_display = ('universo_encuesta', 'persona', 'finalizado')
#     list_filter = ['persona__funcion', 'universo_encuesta__encuesta', 'finalizado']
#     search_fields = ['persona__nombres', 'persona__apellidos', 'persona__funcion', 'persona__rut']


@admin.register(TipoUniversoEncuesta)
class TipoUniversoEncuestaAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'codigo'
    )
    list_filter = ['codigo']
    search_fields = ['codigo']


@admin.register(PeriodoEncuesta)
class PeriodoAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'activo'
    )
    list_filter = ['nombre']
    search_fields = ['nombre']


@admin.register(Encuesta)
class EncuestaAdmin(SummernoteModelAdmin):
    inlines = [PreguntaEncuestaInline]
    summernote_fields = ('descripcion',)
    list_display = (
        'titulo',
        'descripcion',
        'creado_en'
    )
    # list_filter = ['creado_en', ]
    search_fields = ['titulo', 'creado_en']


@admin.register(CategoriaPregunta)
class CategoriaPreguntaAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
    )
    list_filter = ['nombre']
    search_fields = ['nombre']


@admin.register(TipoDescripcionItemPregunta)
class TipoDescripcionItemPreguntaAdmin(admin.ModelAdmin):
    inlines = [DescripcionItemPreguntaInline]
    list_display = (
        'nombre',
        'creado_en'
    )
    list_filter = ['creado_en']
    search_fields = ['nombre']


@admin.register(DescripcionItemPregunta)
class DescripcionItemPreguntaAdmin(admin.ModelAdmin):
    list_display = (
        'descripcion',
        'tipo_descripcion'
    )
    list_filter = ['tipo_descripcion']
    search_fields = ['tipo_descripcion']


@admin.register(PreguntaEncuesta)
class PreguntaEncuestaAdmin(admin.ModelAdmin):
    list_display = (
        'encuesta',
        'categoria',
        'pregunta',
        'es_respuesta_directa',
        'no_mostrar_pregunta',
        'requerida',
        'tipo_respuesta',
        'descripcion_item_pregunta',
        'numero_pregunta',
        'creado_en'
    )
    list_filter = ['categoria', 'es_respuesta_directa', 'requerida']
    search_fields = ['encuesta', 'categoria', 'es_respuesta_directa', 'requerida']


@admin.register(TipoRespuesta)
class TipoRespuestaAdmin(admin.ModelAdmin):
    inlines = [ItemRespuestaInline]
    list_display = (
        'nombre',
        'creado_en'
    )
    list_filter = ['creado_en']
    search_fields = ['creado_en']


@admin.register(Respuesta)
class RespuestaAdmin(admin.ModelAdmin):
    list_display = (
        'respuesta',
        'columna',
        'peso',
        'escrita',
        'check',
        'tipo_respuesta'
    )
    list_filter = ['peso', 'escrita', 'tipo_respuesta']
    search_fields = ['peso', 'escrita', 'tipo_respuesta']


@admin.register(ConfigurarEncuestaUniversoPersona)
class ConfigurarEncuestaUniversoPersonaAdmin(admin.ModelAdmin):
    list_display = (
        'persona',
        'tipo_encuesta',
        'periodo'
    )
    list_filter = ['tipo_encuesta', 'periodo', 'persona']
    search_fields = [
        'periodo__nombre',
        'persona__rut',
        'persona__nombres',
        'persona__apellido_paterno',
        'persona__apellido_materno',
    ]


def generar_universo(modaladmin, request, queryset):
    for ue in queryset:
        ue.generar_encuestas_del_universo()


generar_universo.short_description = u"Generar encuestas del universo"


@admin.register(UniversoEncuesta)
class UniversoEncuestaAdmin(admin.ModelAdmin):
    # inlines = [ItemPersonaUniversoEncuesta]
    actions = [generar_universo]
    list_display = (
        'encuesta',
        'contenido_email',
        'inicio',
        'fin',
        'tipo_encuesta',
        'activar_campo_comentario',
        'creado_en',
        'modificado_en',
        'correos_enviados',
        'creado',
    )
    list_filter = [
        'encuesta',
        'tipo_encuesta',
        'inicio',
        'fin',
        'creado_en',
        'correos_enviados',
        'evaluadores',
    ]
    search_fields = ['nombre', 'activa']


@admin.register(PersonaUniversoEncuesta)
class PersonaUniversoEncuestaAdmin(admin.ModelAdmin):
    list_display = (
        'persona',
        'universo_encuesta',
        'correo_enviado',
        'creado_en',
    )
    list_filter = [
        'universo_encuesta',
        'persona',
    ]
    search_fields = [
        'persona__rut',
        'persona__nombres',
        'persona__apellido_paterno',
        'persona__apellido_materno',
        'universo_encuesta__encuesta__titulo'
    ]


@admin.register(AplicarUniversoEncuestaPersona)
class AplicarUniversoEncuestaPersonaAdmin(admin.ModelAdmin):
    list_display = (
        'universo_encuesta',
        'tipo_encuesta',
        'persona',
        'evaluado',
        'finalizado'
    )
    list_filter = ['tipo_encuesta', 'persona', 'evaluado']
    search_fields = [
        'universo_encuesta__encuesta__titulo',
        'persona__rut',
        'persona__nombres',
        'persona__apellido_paterno',
        'persona__apellido_materno',
        'evaluado__rut',
        'evaluado__nombres',
        'evaluado__apellido_paterno',
        'evaluado__apellido_materno',
    ]


@admin.register(CorreoUniversoEncuesta)
class CorreoUniversoEncuestaAdmin(admin.ModelAdmin):
    list_display = (
        'encabezado',
        'correo',
        'universo_encuesta',
        'enviado',
        'creado_en'
    )
    list_filter = ['universo_encuesta', 'enviado']
    search_fields = ['universo_encuesta']


@admin.register(RespuestaAplicarUniversoEncuestaPersona)
class RespuestaAplicarUniversoEncuestaPersonaAdmin(admin.ModelAdmin):
    list_display = (
        'aplicar_universo_encuesta_persona',
        'pregunta',
        'respuesta',
        'respuesta_directa',
        'creado_en'
    )
    list_filter = ['respuesta', 'aplicar_universo_encuesta_persona__persona']
    search_fields = [
        'aplicar_universo_encuesta_persona__persona__rut',
        'aplicar_universo_encuesta_persona__persona__nombres',
        'aplicar_universo_encuesta_persona__persona__apellido_paterno',
        'aplicar_universo_encuesta_persona__persona__apellido_materno',
        'aplicar_universo_encuesta_persona__evaluado__rut',
        'aplicar_universo_encuesta_persona__evaluado__nombres',
        'aplicar_universo_encuesta_persona__evaluado__apellido_paterno',
        'aplicar_universo_encuesta_persona__evaluado__apellido_materno',
    ]
