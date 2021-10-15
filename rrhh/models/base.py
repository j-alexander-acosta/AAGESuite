from django.db import models

TIPO_SUBVENCION = {
    ('particular', 'Particular'),
    ('particular_subvencionado', 'Particular Subvencionado'),
    ('gratuito', 'Gratuito'),
}
TIPO_CONTRATO = (
    (1, 'Indefinido'),
    (2, 'A plazo'),
    (3, 'Reemplazo'),
)
TIPO_HORA = (
    (1, 'Sostenedor'),
    (2, 'PIE'),
    (3, 'SEP'),
)
TIPO_JORNADA = (
    ('completa', 'Completa'),
    ('media', 'Media'),
    ('noche', 'Noche'),
)
TIPO_FUNCIONARIO = (
    (1, 'Empleado'),
    (2, 'Misionero')
)
TIPO_MISIONERO = (
    (1, 'Licencia misionera'),
    (2, 'Credencial misionera'),
    (2, 'Credencial ministerial')
)
PREVISION_SALUD = (
    (1, 'Fonasa'),
    (2, 'Isapre'),
)
TIPO_ENTREVISTA = (
    (1, 'Felicitaciones'),
    (2, 'Recomendaciones')
)
RAZON_FINIQUITO = (
    (1, 'Término de contrato'),
    (2, 'Finiquito de mutuo acuerdo'),
    (3, 'Finiquito por parte del empleador'),
    (4, 'Renuncia voluntaria'),
)
ESTADO_SOLICITUD = (
    (1, 'Aceptada'),
    (2, 'Pendiente'),
    (3, 'Rechazada'),
    (4, 'En espera de candidatos'),
    (5, 'Pendiente de aprobación'),
    (6, 'Aprobada, lista para contratar'),
    (7, 'Aprobada y contratado')
)
TIPOS_SOLICITUD = (
    (1, 'Contratación'),
    (2, 'Contratación de reemplazo'),
    (3, 'Renovación de contrato'),
    (4, 'Traslado'),
)
ESTADO_CONTRATACION = (
    (1, 'Iniciado'),
    (2, 'Listo para firmar'),
    (3, 'En revisión'),
    (4, 'Firmado'),
)
DOCUMENTO = (
    ('contrato', 'Contrato'),
    ('conocimiento reglamento', 'Toma de conocimiento del Reglamento Interno'),
    ('autorizacion diezmo', 'Autorización de descuento de diezmo'),
    ('autorizacion imagen', 'Autorización de uso de imagen'),
    ('permiso', 'Permiso'),
    ('licencia', 'Licencia'),
    ('finiquito', 'Finiquito'),
    ('perfeccionamiento', 'Perfeccionamiento'),
    ('otro', 'Otro'),
)
TIPO_PERFIL = (
    (1, 'Docente'),
    (2, 'Capellán'),
    (3, 'Jefe de UTP'),
    (4, 'Inspector General'),
    (5, 'Director'),
    (6, 'Departamental'),
    (7, 'Asesor'),
    (8, 'Administrador'),
)


class Perfil(models.Model):
    nombre = models.CharField(max_length=150)
    tipo_perfil = models.PositiveSmallIntegerField(default=1, choices=TIPO_PERFIL, verbose_name='Tipo de perfil')
    descripcion = models.TextField(max_length=550, null=True, blank=True, verbose_name='Descripción')
    solo_lectura = models.BooleanField(default=False, help_text="Marque si el perfil que está creando, será solo para lectura")

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = u'Perfil'
        verbose_name_plural = u'Perfiles'


class Region(models.Model):
    nombre = models.CharField(max_length=150)
    numero = models.PositiveSmallIntegerField(default=0)
    numero_romano = models.CharField(max_length=5, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.title()
        return super(Region, self).save(*args, **kwargs)

    def __str__(self):
        return '{} {}'.format(
            self.numero_romano,
            self.nombre
        )

    class Meta:
        verbose_name = u'Región'
        verbose_name_plural = u'Regiones'
        ordering = ['numero']


class Comuna(models.Model):
    nombre = models.CharField(max_length=150)
    region = models.ForeignKey('Region', on_delete=models.CASCADE, verbose_name='Región')

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.title()
        return super(Comuna, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = u'Comuna'
        verbose_name_plural = u'Comunas'


class Ciudad(models.Model):
    nombre = models.CharField(max_length=150)
    comuna = models.ForeignKey('Comuna', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.title()
        return super(Ciudad, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = u'Ciudad'
        verbose_name_plural = u'Ciudades'


class Banco(models.Model):
    nombre = models.CharField(max_length=250)
    descripcion = models.TextField(max_length=2500, verbose_name='Descripción')

    def __str__(self):
        return '{}'.format(
            self.nombre
        )

    class Meta:
        verbose_name = u'Banco'
        verbose_name_plural = u'Bancos'


class AFP(models.Model):
    nombre = models.CharField(max_length=250)
    descripcion = models.TextField(max_length=2500, verbose_name='Descripción')

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = u'AFP'
        verbose_name_plural = u'AFPs'


class Isapre(models.Model):
    nombre = models.CharField(max_length=250)
    descripcion = models.TextField(max_length=2500, verbose_name='Descripción')

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = u'Isapre'
        verbose_name_plural = u'Isapres'


class Funcion(models.Model):
    TIPO_FUNCION = (
        (1, 'Funcion principal'),
        (2, 'Función secundaria')
    )

    nombre = models.CharField(max_length=250)
    descripcion = models.TextField(max_length=2500, verbose_name='Descripción')
    tipo = models.PositiveSmallIntegerField(default=1, choices=TIPO_FUNCION, verbose_name='Tipo de función')

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = u'Función de empleado'
        verbose_name_plural = u'Funciones de empleados'


class TipoLicencia(models.Model):
    nombre = models.CharField(max_length=250)
    descripcion = models.TextField(max_length=2500, verbose_name='Descripción')
    total_dias = models.IntegerField(verbose_name='Total de días correspondientes')
    dias_habiles = models.BooleanField(default=True, verbose_name='Corresponde a días hábiles')

    def __str__(self):
        return '{} ({}-{})'.format(
            self.nombre,
            self.total_dias,
            '1' if self.dias_habiles else '0'
        )

    class Meta:
        verbose_name = u'Tipo de licencia'
        verbose_name_plural = u'Tipos de licencia'


class TipoDocumento(models.Model):
    nombre = models.CharField(max_length=250)
    descripcion = models.TextField(max_length=2500, verbose_name='Descripción')

    def __str__(self):
        return '{}'.format(
            self.nombre
        )

    class Meta:
        verbose_name = u'Tipo de documento'
        verbose_name_plural = u'Tipos de documento'


class Documento(models.Model):
    perfeccionamiento = models.ForeignKey('Perfeccionamiento', on_delete=models.CASCADE, null=True, blank=True)
    contrato = models.ForeignKey('Contrato', on_delete=models.CASCADE, null=True, blank=True)
    licencia = models.ForeignKey('Licencia', on_delete=models.CASCADE, null=True, blank=True)
    permiso = models.ForeignKey('Permiso', on_delete=models.CASCADE, null=True, blank=True)
    finiquito = models.ForeignKey('Finiquito', on_delete=models.CASCADE, null=True, blank=True)
    tipo_documento = models.CharField(max_length=150, default='otro', choices=DOCUMENTO)
    documento = models.FileField(upload_to="rrhh/documentos")
    fecha_carga = models.DateTimeField(auto_now=True)

    @property
    def get_document_name(self):
        if self.documento:
            return self.documento.name.split('/')[-1]
        else:
            return '-'

    def __str__(self):
        return '{}'.format(
            self.documento.name
        )

    class Meta:
        verbose_name = u'Documento'
        verbose_name_plural = u'Documentos'


class TipoTitulo(models.Model):
    nombre = models.CharField(max_length=250)
    descripcion = models.TextField(max_length=2500, verbose_name='Descripción')

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = u'Tipo de título'
        verbose_name_plural = u'Tipos ded titulos'


class AreaTitulo(models.Model):
    nombre = models.CharField(max_length=250)
    descripcion = models.TextField(max_length=2500, verbose_name='Descripción')

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = u'Área de título'
        verbose_name_plural = u'Areas de titulos'


class Especialidad(models.Model):
    nombre = models.CharField(max_length=250)
    descripcion = models.TextField(max_length=2500, verbose_name='Descripción')
    tipo_titulo = models.ForeignKey("TipoTitulo", on_delete=models.CASCADE, verbose_name="Tipo de título")

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = u'Especialidad'
        verbose_name_plural = u'Especialidades'


class Mencion(models.Model):
    nombre = models.CharField(max_length=250)
    descripcion = models.TextField(max_length=2500, verbose_name='Descripción')
    tipo_titulo = models.ForeignKey("TipoTitulo", on_delete=models.CASCADE, verbose_name="Tipo de título")

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = u'Mención'
        verbose_name_plural = u'Menciones'
