# coding: utf-8
from __future__ import unicode_literals
import hashlib

from django.contrib.humanize.templatetags.humanize import naturalday
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
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


class EscalaValoracion(models.Model):
    aspecto = models.CharField(max_length=100, verbose_name="Aspecto a valorar")
    min = models.PositiveIntegerField(verbose_name="Valor mínimo")
    max = models.PositiveIntegerField(verbose_name="Valor máximo")

    def __str__(self):
        return '{} ({} - {})'.format(
            self.aspecto,
            self.min,
            self.max
        )

    class Meta:
        verbose_name = u'Escala de valoración'
        verbose_name_plural = u'Escalas de valoración'


class Encuesta(models.Model):
    titulo = models.CharField(max_length=255, verbose_name="Título")
    descripcion = models.TextField(verbose_name="Descripción")
    indice_confiabilidad = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, verbose_name="Índice de confiabilidad")
    escala_valoracion = models.ForeignKey("EscalaValoracion", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Escala de valoración")
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


class EscalaDesempeno(models.Model):
    nombre = models.CharField(max_length=250)

    def nivelar(self, nota):
        if nota:
            for n in self.nivel_set.all():
                if n.min <= nota <= n.max:
                    return n.nivel
        return "No tiene nivel"

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = u'Escala de desempeño'
        verbose_name_plural = u'Escalas de desempeño'


class Nivel(models.Model):
    escala_desempeno = models.ForeignKey('EscalaDesempeno', on_delete=models.CASCADE, verbose_name="Escala de desempeño")
    nivel = models.CharField(max_length=100, verbose_name="Nivel de desempeño")
    min = models.DecimalField(max_digits=3, decimal_places=1, verbose_name="Valor mínimo")
    max = models.DecimalField(max_digits=3, decimal_places=1, verbose_name="Valor máximo")

    def __str__(self):
        return '{} ({} - {})'.format(
            self.nivel,
            self.min,
            self.max
        )

    class Meta:
        verbose_name = u'Nivel de desempeño'
        verbose_name_plural = u'Niveles de desempeño'


class UniversoEncuesta(models.Model):
    """
        El tipo de encuesta, en el Universo de encuesta,
        representa el tipo de encuesta a desarrollar (distribución de preguntas y evaluados)
    """
    encuesta = models.ForeignKey("Encuesta", on_delete=models.CASCADE)
    periodo = models.ForeignKey('PeriodoEncuesta', on_delete=models.CASCADE, verbose_name="Grupo de encuesta")
    tipo_encuesta = models.ForeignKey('TipoUniversoEncuesta', on_delete=models.CASCADE, verbose_name="Tipo de encuesta")
    evaluadores = models.ManyToManyField(Persona, verbose_name='Evaluadores')
    escala_desempeno = models.ForeignKey('EscalaDesempeno', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Escala de desempeño")
    contenido_email = models.TextField(verbose_name="Contenido del correo electrónico")
    inicio = models.DateField()
    fin = models.DateField()
    activar_campo_comentario = models.BooleanField(default=False)
    correos_enviados = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de envío de correos")
    creado = models.BooleanField(default=False)
    creado_en = models.DateTimeField(auto_now_add=True)
    modificado_en = models.DateTimeField(auto_now=True)

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

    @property
    def resultados_personas(self):
        return self.resultadopersona_set.all().order_by(
            'persona__infopersona__fundacion'
        ).order_by(
            'persona__infopersona__colegio',
            'nota'
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

    def ponderacion_tipo_encuesta(self, codigo):
        return self.ponderacion_set.filter(tipo_encuesta__codigo=codigo).first().ponderacion

    def get_absolute_url(self):
        return reverse('evado:universo_encuesta_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '{} ({})'.format(
            self.encuesta.titulo,
            self.inicio
        )

    class Meta:
        ordering = ['creado_en']


class Ponderacion(models.Model):
    universo_encuesta = models.ForeignKey('UniversoEncuesta', on_delete=models.CASCADE, verbose_name="Universo de encuestas")
    tipo_encuesta = models.ForeignKey('TipoUniversoEncuesta', on_delete=models.CASCADE, verbose_name="Tipo de encuesta")
    ponderacion = models.PositiveIntegerField(verbose_name="Ponderación")

    def __str__(self):
        return '{}, {} - {}'.format(
            self.universo_encuesta,
            self.tipo_encuesta,
            self.ponderacion
        )

    class Meta:
        unique_together = ['universo_encuesta', 'tipo_encuesta']
        verbose_name = u'Ponderación'
        verbose_name_plural = u'Ponderaciones'


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

    def calcular_resultados(self):
        aueps = AplicarUniversoEncuestaPersona.objects.filter(evaluado=self.evaluado, finalizado__isnull=False)
        # pendientes = aueps.filter(finalizado__isnull=True).exists()
        # if not pendientes:
        rp, created = ResultadoPersona.objects.get_or_create(
            persona=self.evaluado,
            universo_encuesta=self.universo_encuesta
        )
        notas_preguntas = []
        respuestas = RespuestaAplicarUniversoEncuestaPersona.objects.filter(
            aplicar_universo_encuesta_persona__in=aueps,
            respuesta__isnull=False
        ).order_by('pregunta')
        print(self.evaluado)
        if respuestas.exists():
            respuestas_pregunta = respuestas.values(
                'pregunta'
            ).annotate(
                respuestas_cero_autoevaluacion=models.Sum(
                    models.Case(
                        models.When(aplicar_universo_encuesta_persona__tipo_encuesta__codigo='EN0000',
                                    respuesta__peso=0, then=1),
                        default=0,
                        output_field=models.IntegerField()
                    )
                ),
                total_autoevaluacion=models.Sum(
                    models.Case(
                        models.When(aplicar_universo_encuesta_persona__tipo_encuesta__codigo='EN0000',
                                    respuesta__peso__gte=1, then=1),
                        default=0,
                        output_field=models.IntegerField()
                    )
                ),
                suma_autoevaluacion=models.Sum(
                    models.Case(
                        models.When(aplicar_universo_encuesta_persona__tipo_encuesta__codigo='EN0000', then='respuesta__peso'),
                        default=0,
                        output_field=models.IntegerField()
                    )
                ),
                respuestas_cero_pares=models.Sum(
                    models.Case(
                        models.When(aplicar_universo_encuesta_persona__tipo_encuesta__codigo='EN0001',
                                    respuesta__peso=0, then=1),
                        default=0,
                        output_field=models.IntegerField()
                    )
                ),
                total_pares=models.Sum(
                    models.Case(
                        models.When(aplicar_universo_encuesta_persona__tipo_encuesta__codigo='EN0001',
                                    respuesta__peso__gte=1, then=1),
                        default=0,
                        output_field=models.IntegerField()
                    )
                ),
                suma_pares=models.Sum(
                    models.Case(
                        models.When(aplicar_universo_encuesta_persona__tipo_encuesta__codigo='EN0001', then='respuesta__peso'),
                        default=0,
                        output_field=models.IntegerField()
                    )
                ),
                respuestas_cero_directivos=models.Sum(
                    models.Case(
                        models.When(aplicar_universo_encuesta_persona__tipo_encuesta__codigo='EN0003',
                                    respuesta__peso=0, then=1),
                        default=0,
                        output_field=models.IntegerField()
                    )
                ),
                total_directivos=models.Sum(
                    models.Case(
                        models.When(aplicar_universo_encuesta_persona__tipo_encuesta__codigo='EN0003',
                                    respuesta__peso__gte=1, then=1),
                        default=0,
                        output_field=models.IntegerField()
                    )
                ),
                suma_directivos=models.Sum(
                    models.Case(
                        models.When(aplicar_universo_encuesta_persona__tipo_encuesta__codigo='EN0003', then='respuesta__peso'),
                        default=0,
                        output_field=models.IntegerField()
                    )
                )
            )
            for r in respuestas_pregunta:
                print(r)
                pregunta = get_object_or_404(PreguntaEncuesta, id=r['pregunta'])
                rpp, rpp_created = ResultadoPreguntaPersona.objects.get_or_create(
                    resultado_persona=rp,
                    pregunta=pregunta
                )
                respuestas_cero_auto = r['respuestas_cero_autoevaluacion'] if r['respuestas_cero_autoevaluacion'] <= 3 else 3
                respuestas_cero_pares = r['respuestas_cero_pares'] if r['respuestas_cero_pares'] <= 3 else 3
                respuestas_cero_directivos = r['respuestas_cero_directivos'] if r['respuestas_cero_directivos'] <= 3 else 3

                total_autoevaluacion = r['total_autoevaluacion'] + respuestas_cero_auto
                total_pares = (r['total_pares'] + respuestas_cero_pares)
                total_directivos = r['total_directivos'] + respuestas_cero_directivos

                rpp.promedio_autoevaluacion = r['suma_autoevaluacion'] / total_autoevaluacion if total_autoevaluacion > 0 else 0
                rpp.promedio_pares = r['suma_pares'] / total_pares if total_pares > 0 else 0
                rpp.promedio_directivos = r['suma_directivos'] / total_directivos if total_directivos > 0 else 0

                hay_autoevaluacion = True
                hay_pares = True
                if rpp.promedio_autoevaluacion == 0:
                    hay_autoevaluacion = False
                if rpp.promedio_pares == 0:
                    hay_pares = False

                print(rpp.promedio_directivos)
                print(rpp.promedio_pares)
                print(rpp.promedio_autoevaluacion)

                ponderaciones = self.universo_encuesta.ponderacion_set.all()
                for ponderacion in ponderaciones:
                    ponde = ponderacion.ponderacion
                    print("AQUI")
                    print(self.universo_encuesta.ponderacion_tipo_encuesta("EN0001"))
                    if ponderacion.tipo_encuesta.codigo == 'EN0000':
                        if not hay_pares:
                            ponde += self.universo_encuesta.ponderacion_tipo_encuesta("EN0001")
                        rpp.peso_autoevaluacion = rpp.promedio_autoevaluacion * (ponde / 100)
                    if ponderacion.tipo_encuesta.codigo == 'EN0001':
                        if not hay_autoevaluacion:
                            ponde += self.universo_encuesta.ponderacion_tipo_encuesta("EN0000")
                        rpp.peso_pares = rpp.promedio_pares * (ponde / 100)
                    if ponderacion.tipo_encuesta.codigo == 'EN0003':
                        if not hay_pares and not hay_autoevaluacion:
                            ponde += self.universo_encuesta.ponderacion_tipo_encuesta("EN0000") + self.universo_encuesta.ponderacion_tipo_encuesta("EN0001")
                        rpp.peso_directivos = rpp.promedio_directivos * (ponde / 100)

                print(rpp.peso_directivos)
                print(rpp.peso_pares)
                print(rpp.peso_autoevaluacion)

                rpp.nota = rpp.peso_autoevaluacion + rpp.peso_pares + rpp.peso_directivos
                rpp.save()
                notas_preguntas.append(rpp.nota)

            rp.nota = sum(notas_preguntas) / len(notas_preguntas)
            rp.save()

    def save(self, *args, **kwargs):
        super(AplicarUniversoEncuestaPersona, self).save(*args, **kwargs)
        self.calcular_resultados()

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


class ResultadoPersona(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    universo_encuesta = models.ForeignKey('UniversoEncuesta', on_delete=models.CASCADE)
    nota = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True, verbose_name="Nota final")

    @property
    def nota_dimension_tipoencuesta(self):
        return self.resultadopreguntapersona_set.all().values(
            'pregunta__categoria__nombre'
        ).annotate(
            promedio_directivos=models.Avg('promedio_directivos'),
            puntaje_directivos=models.Avg('peso_directivos'),
            promedio_pares=models.Avg('promedio_pares'),
            puntaje_pares=models.Avg('peso_pares'),
            promedio_autoevaluacion=models.Avg('promedio_autoevaluacion'),
            puntaje_autoevaluacion=models.Avg('peso_autoevaluacion'),
            nota=models.Avg('nota')
        )

    @property
    def get_nivel(self):
        return self.universo_encuesta.escala_desempeno.nivelar(self.nota)

    def __str__(self):
        return '{} {}'.format(
            self.persona,
            self.universo_encuesta,
        )

    class Meta:
        verbose_name = u'Resultado de encuesta de persona'
        verbose_name_plural = u'Resultados de encuestas de personas'


class ResultadoPreguntaPersona(models.Model):
    resultado_persona = models.ForeignKey('ResultadoPersona', on_delete=models.CASCADE)
    pregunta = models.ForeignKey('PreguntaEncuesta', on_delete=models.CASCADE)
    promedio_autoevaluacion = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True, verbose_name="Promedio de autoevaluación")
    peso_autoevaluacion = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True, verbose_name="Peso de autoevaluación")
    promedio_pares = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True, verbose_name="Promedio de pares")
    peso_pares = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True, verbose_name="Promedio de pares")
    promedio_directivos = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True, verbose_name="Promedio de directivos")
    peso_directivos = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True, verbose_name="Promedio de directivos")
    nota = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)

    def __str__(self):
        return '{} - {}'.format(
            self.resultado_persona,
            self.pregunta
        )

    class Meta:
        verbose_name = u'Resultado de pregunta de persona'
        verbose_name_plural = u'Resultados de preguntas de personas'
