# coding: utf-8
from __future__ import unicode_literals
import hashlib

from django.contrib.humanize.templatetags.humanize import naturalday
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils import timezone
from django.db import models
from random import getrandbits
from rrhh.models import Persona


def generate_hash():
    hash = "%032x"
    return hashlib.sha512(hash.encode('utf-8') % getrandbits(160)).hexdigest()


class InfoPersona(models.Model):
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE)
    funcion = models.CharField(max_length=100, null=True, blank=True)
    colegio = models.CharField(max_length=100, null=True, blank=True)
    fundacion = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return ''.format(self.persona)

    class Meta:
        verbose_name = 'Información extra de Persona'
        verbose_name_plural = 'Información extra de Personas'


class ConfigurarEncuestaUniversoPersona(models.Model):
    """
        El tipo de encuesta, en la configuración de evaluados, representa a que tipo de evaluación responde ésta
        y sirve para el cálculo y generación de reportes
    """
    persona = models.ForeignKey(Persona, related_name="persona", on_delete=models.CASCADE, verbose_name='Evaluador')
    evaluados = models.ManyToManyField(Persona, related_name="evaluados")
    periodo = models.ForeignKey('PeriodoEncuesta', on_delete=models.CASCADE, null=True, verbose_name="Grupo de encuesta")
    tipo_encuesta = models.ForeignKey('TipoUniversoEncuesta', on_delete=models.CASCADE, verbose_name="Tipo de encuesta")
    creado_en = models.DateTimeField(auto_now_add=True)
    modificado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} - {} ({})'.format(
            self.persona,
            self.tipo_encuesta,
            self.periodo
        )


class Encuesta(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(verbose_name="Descripción")
    creado_en = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('evado:encuesta_detail', kwargs={'pk': self.pk})

    @property
    def obtener_preguntas_no_respuesta_directa(self):
        return self.preguntaencuesta_set.filter(es_respuesta_directa=False).order_by('categoria', 'numero_pregunta')

    @property
    def obtener_preguntas_respuesta_directa(self):
        return self.preguntaencuesta_set.filter(es_respuesta_directa=True)

    def __str__(self):
        return '{}'.format(
            self.titulo,
        )


class CategoriaPregunta(models.Model):
    nombre = models.CharField(max_length=255)

    def get_absolute_url(self):
        return reverse('evado:categoria_pregunta_list')

    def __str__(self):
        return '{}'.format(
            self.nombre,
        )


class TipoDescripcionItemPregunta(models.Model):
    nombre = models.CharField(max_length=255)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}'.format(
            self.nombre,
        )


class DescripcionItemPregunta(models.Model):
    descripcion = models.TextField(verbose_name="Descripción")
    tipo_descripcion = models.ForeignKey('TipoDescripcionItemPregunta', on_delete=models.CASCADE,
                                         verbose_name="Tipo de descripción")
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}'.format(
            self.descripcion,
        )


class PreguntaEncuesta(models.Model):
    encuesta = models.ForeignKey("Encuesta", on_delete=models.CASCADE)
    categoria = models.ForeignKey("CategoriaPregunta", on_delete=models.CASCADE)
    pregunta = models.TextField()
    es_respuesta_directa = models.BooleanField(default=False)
    no_mostrar_pregunta = models.BooleanField(default=False)
    requerida = models.BooleanField(default=True, verbose_name="Es requerida")
    tipo_respuesta = models.ForeignKey(
        "TipoRespuesta",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name="Tipo de respuesta"
    )
    descripcion_item_pregunta = models.ForeignKey(
        "TipoDescripcionItemPregunta", null=True, blank=True,
        on_delete=models.CASCADE,
        verbose_name="Descripción de ítem de pregunta"
    )
    numero_pregunta = models.PositiveIntegerField(verbose_name="Número de pregunta")
    creado_en = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('evado:pregunta_encuesta_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '{}. {} ({})'.format(
            self.numero_pregunta,
            self.pregunta,
            self.encuesta.titulo
        )


class TipoRespuesta(models.Model):
    nombre = models.CharField(max_length=150)
    encabezado = models.CharField(
        max_length=150,
        default="Escala de valoración",
        help_text="Este encabezado, aparecera en la encuesta como cabecera de las respuestas")
    creado_en = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('evado:tipo_respuesta_list')

    def __str__(self):
        return '{}'.format(
            self.nombre,
        )


class Respuesta(models.Model):
    respuesta = models.CharField(max_length=255)
    columna = models.PositiveIntegerField(default=1)
    peso = models.IntegerField(default=0)
    escrita = models.BooleanField(default=False, verbose_name="Es escrita")
    check = models.BooleanField(default=False, verbose_name="Es seleccionable")
    tipo_respuesta = models.ForeignKey('TipoRespuesta', on_delete=models.CASCADE, verbose_name="Tipo de respuesta")

    def get_absolute_url(self):
        return reverse('evado:respuesta_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '{}'.format(
            self.respuesta,
        )


PERIODO_CHOICE = (
    ('verano', 'Verano'),
    ('primer_semestre', 'Primer Semestre'),
    ('invierno', 'Invierno'),
    ('segundo_semestre', 'Segundo Semestre'),
)


class PeriodoEncuesta(models.Model):
    nombre = models.CharField(max_length=20)
    anio = models.PositiveIntegerField(default=2021, verbose_name="Año")
    periodo = models.CharField(max_length=25, choices=PERIODO_CHOICE, null=True, blank=True)
    activo = models.BooleanField(default=False)

    def clean(self, *args, **kwargs):
        if self.activo and PeriodoEncuesta.objects.filter(activo=True).count() > 0:
            raise ValidationError('Ya existe un grupo activo.')
        super(PeriodoEncuesta, self).clean(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('evado:periodo_list')

    @property
    def get_full_periodo(self):
        if self.periodo or self.anio:
            periodo = '{} {}'.format(
                self.get_periodo_display() if self.periodo else '',
                self.anio if self.anio else ''
            )
        else:
            periodo = '-'
        return periodo

    def __str__(self):
        return '{}'.format(
            self.nombre
        )


class TipoUniversoEncuesta(models.Model):
    CODIGO_AUTO = "EN0000"
    CODIGO_PARES = "EN0001"
    CODIGO_PERSONALIZADA = "EN0002"
    CODIGO_SUPERIOR = "EN0003"

    CODIGO_CHOICES = (
        (CODIGO_AUTO, "Autoevaluación"),
        (CODIGO_PARES, "Evaluación de Pares"),
        (CODIGO_PERSONALIZADA, "Evaluación Personalizada"),
        (CODIGO_SUPERIOR, "Evaluación desde Superiores"),
    )

    nombre = models.CharField(max_length=255)
    codigo = models.CharField(max_length=10, choices=CODIGO_CHOICES, verbose_name="Tipo de Configuración")

    def __str__(self):
        return self.nombre


class UniversoEncuesta(models.Model):
    """
        El tipo de encuesta, en el Universo de encuesta,
        representa el tipo de encuesta a desarrollar (distribucion de preguntas y evaluados)
    """
    encuesta = models.ForeignKey("Encuesta", on_delete=models.CASCADE)
    evaluadores = models.ManyToManyField(Persona, verbose_name='Evaluadores')
    contenido_email = models.TextField(verbose_name="Contenido del correo electrónico")
    inicio = models.DateField()
    fin = models.DateField()
    tipo_encuesta = models.ForeignKey('TipoUniversoEncuesta', on_delete=models.CASCADE, verbose_name="Tipo de encuesta")
    periodo = models.ForeignKey('PeriodoEncuesta', on_delete=models.CASCADE, verbose_name="Grupo de encuesta")
    activar_campo_comentario = models.BooleanField(default=False)
    creado_en = models.DateTimeField(auto_now_add=True)
    modificado_en = models.DateTimeField(auto_now=True)
    correos_enviados = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de envío de correos")
    creado = models.BooleanField(default=False)

    @property
    def periodo_activo(self):
        return 'habilitada desde {} hasta {}'.format(
            naturalday(self.inicio),
            naturalday(self.fin)
        )

    @property
    def total_evaluadores(self):
        return self.evaluadores.all().count()

    @property
    def total_evaluaciones(self):
        total_evaluaciones = 0
        for evaluador in self.evaluadores.all():
            configs = ConfigurarEncuestaUniversoPersona.objects.filter(persona=evaluador, periodo=self.periodo)
            for confi in configs:
                total_evaluaciones += confi.evaluados.all().count()
        return total_evaluaciones

    @property
    def total_finalizadas(self):
        return self.aplicaruniversoencuestapersona_set.filter(finalizado__isnull=False).count()

    def generar_encuestas_del_universo(self):
        if not self.creado:
            self.generar_encuestas_segun_tipo(self)
            self.creado = True
            self.save()

    def generar_encuestas_segun_tipo(self, cursos_formulario=None):
        """
        <aues> tipo:list. Objetos AplicarUniversoEncuestaPersona.
        """
        aues = ''
        if self.tipo_encuesta.codigo == TipoUniversoEncuesta.CODIGO_AUTO:
            aues = self.aplicar_encuesta_tipo_normal()

        elif self.tipo_encuesta.codigo == TipoUniversoEncuesta.CODIGO_PERSONALIZADA:
            aues = self.aplicar_encuesta_tipo_personalizada()

        self.generar_preguntas_para_aues(aues)

    def generar_preguntas_para_aues(self, aues):
        preguntas = self.encuesta.preguntaencuesta_set.all()
        for aue in aues:
            lista_respuestas = []
            preguntas_aue_ids = aue.respuestaaplicaruniversoencuestapersona_set.all().values_list('pregunta__id')
            preguntas_existentes = PreguntaEncuesta.objects.filter(id__in=preguntas_aue_ids)
            for p in preguntas:
                if p.requerida and p not in preguntas_existentes:
                    lista_respuestas.append(
                        RespuestaAplicarUniversoEncuestaPersona(aplicar_universo_encuesta_persona=aue, pregunta=p))
            RespuestaAplicarUniversoEncuestaPersona.objects.bulk_create(lista_respuestas)

    def aplicar_encuesta_tipo_normal(self):
        # preguntas = self.encuesta.preguntaencuesta_set.all()
        aues = []
        for x in self.evaluadores.all():
            aue, created = AplicarUniversoEncuestaPersona.objects.get_or_create(universo_encuesta=self, persona=x)
            if created:
                aues.append(aue)
        return aues

    def aplicar_encuesta_tipo_personalizada(self):
        """
            Esta Funcion, crea los registros para la toma de la encuesta (Aplicar Universo Encuesta Persona)
            El Periodo es la clave para la creación de la encuesta
            y permanencia de distintas configuraciones con el mismo evaluador.
            así al seleccionar un evaluador (Persona),
            solo se considerarán las configuraciones pertenecientes al periodo del Universo de Encuestas
            y no se crearán encuestas para todas las configuraciones de este evaluador
        :return: Diccionario de Aplicar Universo Encuesta Persona
        """
        aues = []
        # preguntas = self.encuesta.preguntaencuesta_set.all()
        for evaluador in self.evaluadores.all():
            configs = ConfigurarEncuestaUniversoPersona.objects.filter(persona=evaluador, periodo=self.periodo)
            for cup in configs:
                for x in cup.evaluados.all():
                    aue, created = AplicarUniversoEncuestaPersona.objects.get_or_create(
                        universo_encuesta=self,
                        persona=cup.persona,
                        evaluado=x,
                        tipo_encuesta=cup.tipo_encuesta
                    )
                    """ Aquí solo se crean las auep, al ingresar a la encuesta, se cargar las preguntas para cada auep,
                    asi el servidor no se colapsa al crear un nuevo universo """
                    # if created or RespuestaAplicarUniversoEncuestaPersona.objects.filter(aplicar_universo_encuesta_persona=aue).count() < preguntas.count():
                    #     aues.append(aue)
        return aues

    @property
    def itemes_personas(self):
        return self.personauniversoencuesta_set.all().order_by(
            'persona__infopersona__fundacion'
        ).order_by(
            'persona__infopersona__colegio',
            'encuesta_finalizada',
            'persona'
        )

    def ultima_pregunta_respondida(self, persona):
        ultima_pregunta = None
        for auep in self.aplicaruniversoencuestapersona_set.filter(persona=persona):
            pregunta = auep.respuestaaplicaruniversoencuestapersona_set.filter(respuesta__isnull=True)
            if pregunta:
                pregunta = pregunta.order_by('pregunta__numero_pregunta').first().pregunta
                if ultima_pregunta and pregunta.numero_pregunta < ultima_pregunta.numero_pregunta:
                    ultima_pregunta = pregunta
                else:
                    ultima_pregunta = pregunta
        return ultima_pregunta

    def get_absolute_url(self):
        return reverse('evado:universo_encuesta_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '{} ({})'.format(
            self.encuesta.titulo,
            self.inicio
        )

    class Meta:
        ordering = ['creado_en']


class PersonaUniversoEncuesta(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    universo_encuesta = models.ForeignKey("UniversoEncuesta", on_delete=models.CASCADE,
                                          verbose_name="Universo de encuestas")
    correo_enviado = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de envío de correo")
    encuesta_finalizada = models.DateTimeField(null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    @property
    def get_hash_encuesta(self):
        return AplicarUniversoEncuestaPersona.objects.filter(
            universo_encuesta=self.universo_encuesta,
            persona=self.persona
        ).first().hash

    @property
    def mail_enviado(self):
        if self.correo_enviado:
            return True
        else:
            return False

    def ha_finalizado(self):
        finalizado = True
        for auep in AplicarUniversoEncuestaPersona.objects.filter(
                universo_encuesta=self.universo_encuesta,
                persona=self.persona
        ):
            if not auep.finalizado:
                finalizado = False
                break

        if finalizado:
            self.encuesta_finalizada = timezone.now()
            self.save()

    @property
    def total_encuestas(self):
        return AplicarUniversoEncuestaPersona.objects.filter(
            universo_encuesta=self.universo_encuesta,
            persona=self.persona
        ).count()

    def __str__(self):
        return '{}'.format(
            self.persona
        )

    class Meta:
        ordering = ['id']


class AplicarUniversoEncuestaPersona(models.Model):
    universo_encuesta = models.ForeignKey('UniversoEncuesta', on_delete=models.CASCADE)
    tipo_encuesta = models.ForeignKey('TipoUniversoEncuesta', on_delete=models.CASCADE, verbose_name="Tipo de encuesta")
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    evaluado = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='evaluado')
    hash = models.CharField('hash', max_length=128, default=generate_hash, unique=True, null=True)
    comentario = models.TextField(null=True, blank=True)
    finalizado = models.DateTimeField(null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    @property
    def total_respuestas(self):
        return sum(map(lambda x: x.respuesta.peso,
                       self.respuestaaplicaruniversoencuestapersona_set.filter(pregunta__es_respuesta_directa=False,
                                                                               respuesta__isnull=False)))

    @property
    def respuestas_contestadas(self):
        return self.respuestaaplicaruniversoencuestapersona_set.exclude(respuesta=None)

    @property
    def respuestas_finalizado(self):
        return self.respuestaaplicaruniversoencuestapersona_set.filter(respuesta__isnull=False).filter(
            respuesta__check=False, respuesta__escrita=False)

    @property
    def nombre(self):
        code = self.universo_encuesta.tipo_encuesta.codigo
        name = ""
        if code == TipoUniversoEncuesta.CODIGO_AUTO:
            name = u"%s" % self.universo_encuesta.encuesta.titulo
        elif code == TipoUniversoEncuesta.CODIGO_PERSONALIZADA:
            name = u""
        return name

    def get_absolute_url(self):
        return reverse('evado:aplicar_universo_encuesta_persona_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '{} - {} ({}) > {}'.format(
            self.persona,
            self.universo_encuesta,
            self.universo_encuesta.tipo_encuesta,
            self.evaluado
        )


class RespuestaAplicarUniversoEncuestaPersona(models.Model):
    aplicar_universo_encuesta_persona = models.ForeignKey('AplicarUniversoEncuestaPersona', on_delete=models.CASCADE)
    pregunta = models.ForeignKey('PreguntaEncuesta', on_delete=models.CASCADE)
    respuesta = models.ForeignKey('Respuesta', on_delete=models.SET_NULL, null=True, blank=True)
    respuesta_directa = models.TextField(null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('evado:respuesta_aplicar_universo_encuesta_persona_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = u"Respuesta a Encuesta"
        verbose_name_plural = u"Respuestas a Encuestas"


class CorreoUniversoEncuesta(models.Model):
    encabezado = models.CharField(max_length=255)
    correo = models.TextField()
    universo_encuesta = models.ForeignKey('UniversoEncuesta', on_delete=models.CASCADE)
    enviado = models.DateTimeField(null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = u"Correo Universo Encuesta"
        verbose_name_plural = u"Correos de universos de encuestas"

    def __str__(self):
        return '{} - {}'.format(
            self.encabezado,
            self.universo_encuesta
        )

    def get_absolute_url(self):
        return reverse('evado:correo_universo_detail', kwargs={'pk': self.pk})
