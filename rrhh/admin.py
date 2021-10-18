from django.contrib import admin
from rrhh.models import *


@admin.register(persona.Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display = (
        'rut',
        'full_name',
    )
    search_fields = ['rut', 'nombres', 'apellido_paterno', 'apellido_materno']
    list_filter = ['religion', 'titulado', 'nacionalidad', 'profesion']


@admin.register(persona.PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = (
        'usuario',
        'perfil',
        'nivel_acceso'
    )
    search_fields = ['usuario']
    list_filter = ['nivel_acceso', 'perfil']


@admin.register(persona.Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = (
        'persona',
        'estado',
    )
    search_fields = ['persona__rut', 'persona__get_full_name']
    list_filter = ['afp', 'salud', 'isapre', 'estado', 'tipo_misionero']


@admin.register(entidad.Entidad)
class EntidadAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'tipo_entidad',
        'dependiente'
    )
    search_fields = ['nombre', 'abrev', 'direccion']
    list_filter = ['dependiente']


@admin.register(entidad.DetalleColegio)
class DetalleColegioAdmin(admin.ModelAdmin):
    list_display = (
        'colegio',
        'rbd',
        'tipo_subvencion'
    )
    search_fields = ['colegio__nombre', 'rbd', 'direccion']
    list_filter = ['tipo_subvencion', 'tipo_jornada', 'colegio__dependiente']


@admin.register(entidad.Vacacion)
class VacacionAdmin(admin.ModelAdmin):
    list_display = (
        'contrato',
        'total_dias',
        'fecha_inicio'
    )
    search_fields = ['contrato__persona__rut', 'contrato__persona__get_full_name']


@admin.register(entidad.Licencia)
class LicenciaAdmin(admin.ModelAdmin):
    list_display = (
        'contrato',
        'tipo_licencia',
        'tipo_licencia_descripcion',
        'folio_licencia'
    )
    search_fields = [
        'contrato__persona__rut',
        'contrato__persona__get_full_name',
        'tipo_licencia__nombre',
        'tipo_licencia_descripcion'
    ]
    list_filter = ['tipo_licencia']


@admin.register(entidad.Permiso)
class PermisoAdmin(admin.ModelAdmin):
    list_display = (
        'contrato',
        'observaciones',
        'total_dias'
    )
    search_fields = [
        'contrato__persona__rut',
        'contrato__persona__get_full_name',
    ]
    list_filter = ['goce_sueldo']


@admin.register(entidad.Contrato)
class ContratoAdmin(admin.ModelAdmin):
    list_display = (
        'funcionario',
        'entidad',
        'categoria',
        #'vigente'
    )
    search_fields = [
        'funcionario__persona__rut',
        'funcionario__persona__get_full_name',
        'entidad__nombre'
    ]
    list_filter = [
        'entidad',
        'categoria',
        'tipo_contrato'
    ]


@admin.register(entidad.Finiquito)
class FiniquitoAdmin(admin.ModelAdmin):
    list_display = (
        'contrato',
        'razon_baja',
    )
    search_fields = ['contrato__persona__rut']


@admin.register(entidad.Entrevista)
class EntrevistaAdmin(admin.ModelAdmin):
    list_display = (
        'contrato',
        'tipo',
    )
    search_fields = ['contrato__persona__rut']


@admin.register(entidad.Solicitud)
class SolicitudAdmin(admin.ModelAdmin):
    list_display = (
        'entidad',
        'cargo',
    )
    search_fields = ['entidad', 'cargo']
    list_filter = ['entidad']


@admin.register(entidad.EstadoSolicitud)
class EstadoSolicitudAdmin(admin.ModelAdmin):
    list_display = (
        'solicitud',
        'estado',
    )
    search_fields = ['solicitud__entidad']
    list_filter = ['solicitud__entidad']


@admin.register(entidad.EstadoContratacion)
class EstadoContratacionAdmin(admin.ModelAdmin):
    list_display = (
        'contrato',
        'estado',
    )
    search_fields = ['contrato', 'contrato__entidad', 'contrato__funcionario']
    list_filter = ['contrato__entidad', 'estado']


@admin.register(entidad.Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = (
        'tipo_documento',
        'fecha_carga',
    )
    search_fields = [
        'tipo_documento',
        'contrato__entidad',
        'contrato__funcionario__persona',
        'finiquito__contrato__entidad',
        'finiquito__contrato__funcionario__persona',
        'permiso__contrato__entidad',
        'permiso__contrato__funcionario__persona',
        'licencia__contrato__entidad',
        'licencia__contrato__funcionario__persona',
        'perfeccionamiento__persona',
        'perfeccionamiento__titulo',
    ]
    list_filter = ['tipo_documento']
