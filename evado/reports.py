import os
from io import BytesIO
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.defaultfilters import floatformat
from reportlab.lib import colors, utils
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet, _baseFontNameB, _baseFontNameI
from reportlab.lib.units import cm
from reportlab.platypus import Frame, NextPageTemplate, PageTemplate
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image

from django.conf import settings
from evado.models import Ponderacion
from rrhh.templatetags.rrhh_utils import get_real_month

if settings.DEBUG:
    PATH_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)))
else:
    PATH_FILE = os.path.join(os.path.dirname(__file__))

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="MyTitle", parent=styles['Title'], leading=9, fontSize=14))
styles.add(ParagraphStyle(name="MyNormal", parent=styles['Normal'], alignment=TA_JUSTIFY, fontSize=10))
styles.add(ParagraphStyle(name="SubTitle", parent=styles['MyNormal'], alignment=TA_CENTER))
styles.add(ParagraphStyle(name="Header", parent=styles['SubTitle'], textColor=colors.lightslategray))
styles.add(ParagraphStyle(name="TextRight", parent=styles['MyNormal'], alignment=TA_RIGHT))
styles.add(ParagraphStyle(name="NormalBold", parent=styles['MyNormal'], fontName=_baseFontNameB, textTransform='uppercase'))
styles.add(ParagraphStyle(name="TableDefinition", parent=styles['MyNormal'], fontName=_baseFontNameI, fontSize=9,))

estilo_tabla = TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.aliceblue),
    ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
    ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
])


def agregar_parrafo(story, parrafo, estilo, espacio_final):
    data = Paragraph(parrafo, estilo)
    story.append(data)
    story.append(espacio_final)

    return story


def generar_pdf_resultados(resultado_persona, story):

    story.append(NextPageTemplate('contenido'))
    story = agregar_parrafo(story, resultado_persona.persona.infopersona.fundacion, styles['MyTitle'], Spacer(0, 8))
    story = agregar_parrafo(story, resultado_persona.persona.infopersona.colegio, styles['MyTitle'], Spacer(0, 8))
    story = agregar_parrafo(story, "Informe Individual", styles['SubTitle'], Spacer(0, 30))

    saludo = "Estimado/a <b>{}</b>, reciba un cordial saludo.".format(
        resultado_persona.persona.get_full_name()
    )
    story = agregar_parrafo(story, saludo, styles['MyNormal'], Spacer(0, 10))

    intro = "Durante el mes de {} del año {} se realizó en todo el Sistema Educativo Adventista (SEA) " \
            "el proceso de {} en el cual participaron todos los profesores del SEA.".format(
        get_real_month(resultado_persona.universo_encuesta.inicio.month),
        resultado_persona.universo_encuesta.inicio.year,
        resultado_persona.universo_encuesta.encuesta.titulo,
    )
    story = agregar_parrafo(story, intro, styles['MyNormal'], Spacer(0, 10))

    descripcion = "En este primer año de implementación actuaron como evaluadores los miembros del equipo directivo de su establecimiento," \
                  " un grupo de docentes pares de su mismo nivel de enseñanza y su propia autoevaluación."
    story = agregar_parrafo(story, descripcion, styles['MyNormal'], Spacer(0, 10))

    instrumento = "El instrumento aplicado, es un instrumento creado para el contexto del SEA con el siguiente índice de confiabilidad {}.".format(
        resultado_persona.universo_encuesta.encuesta.indice_confiabilidad
    )
    story = agregar_parrafo(story, instrumento, styles['MyNormal'], Spacer(0, 10))

    escala = "El cual tiene una escala de valoración de {} a {} siendo {} el valor que refleja" \
             " en menor medida el {} y {} el {} mayor.".format(
        resultado_persona.universo_encuesta.encuesta.escala_valoracion.min,
        resultado_persona.universo_encuesta.encuesta.escala_valoracion.max,
        resultado_persona.universo_encuesta.encuesta.escala_valoracion.min,
        resultado_persona.universo_encuesta.encuesta.escala_valoracion.aspecto,
        resultado_persona.universo_encuesta.encuesta.escala_valoracion.max,
        resultado_persona.universo_encuesta.encuesta.escala_valoracion.aspecto,
    )
    story = agregar_parrafo(story, escala, styles['MyNormal'], Spacer(0, 10))

    ponderaciones = ""
    ponderaciones_queryset = Ponderacion.objects.filter(
        universo_encuesta=resultado_persona.universo_encuesta).order_by('-tipo_encuesta__codigo')
    for index, p in enumerate(ponderaciones_queryset):
        if index != 0:
            if index < (ponderaciones_queryset.count() - 1):
                ponderaciones = ponderaciones + ", "
            else:
                ponderaciones = ponderaciones + " y "
        ponderaciones = ponderaciones + "{}% {}".format(p.ponderacion, p.tipo_encuesta.nombre)
    exp_calificacion = "El puntaje final obtenido es equivalente al promedio de las calificaciones asignadas por los " \
                       "evaluadores, ponderado de la siguiente manera: {}." \
                       " El resultado final, posiciona al docente en alguna de los siguientes niveles de desempeño.".format(
        ponderaciones
    )
    story = agregar_parrafo(story, exp_calificacion, styles['MyNormal'], Spacer(0, 10))

    niveles_desempeno = resultado_persona.universo_encuesta.escala_desempeno.nivel_set.all()
    datos = [
        [Paragraph("Niveles de Desempeño", styles['SubTitle']),
         Paragraph("Escala", styles['SubTitle'])]
    ]
    for n in niveles_desempeno:
        linea = ['{}'.format(n.nivel), Paragraph('{} - {}'.format(n.min, n.max), styles['SubTitle'])]
        datos.append(linea)
    tabla_niveles = Table(datos, colWidths=[310, 150], rowHeights=15)
    tabla_niveles.setStyle(estilo_tabla)
    story.append(tabla_niveles)
    story.append(Spacer(0, 20))

    encabezado_notas = "A continuación, entregamos sus resultados por dimensión y grupos de evaluadores:"
    story = agregar_parrafo(story, encabezado_notas, styles['MyNormal'], Spacer(0, 10))

    notas = resultado_persona.nota_dimension_tipoencuesta
    datos = []
    primera_fila = [Paragraph("Dimensiones", styles['SubTitle'])]
    for p in ponderaciones_queryset:
        if p.tipo_encuesta.codigo == "EN0003":
            te = "Directivos"
        elif p.tipo_encuesta.codigo == "EN0001":
            te = "Pares"
        else:
            te = "Autoevaluación"
        enc = Paragraph('{} {}%'.format(te, p.ponderacion), styles['SubTitle'])
        primera_fila.append(enc)
    primera_fila.append(Paragraph("Nota Final", styles['SubTitle']))
    datos.append(primera_fila)
    for n in notas:
        linea = [
            '{}'.format(n['pregunta__categoria__nombre']),
            Paragraph('{}'.format(floatformat(n['puntaje_directivos']), 1), styles['SubTitle']),
            Paragraph('{}'.format(floatformat(n['puntaje_pares']), 1), styles['SubTitle']),
            Paragraph('{}'.format(floatformat(n['puntaje_autoevaluacion']), 1), styles['SubTitle']),
            Paragraph('{}'.format(floatformat(n['nota']), 1), styles['SubTitle'])
        ]
        datos.append(linea)
    tabla_notas = Table(datos, colWidths=[200, 70, 50, 90, 50])
    tabla_notas.setStyle(estilo_tabla)
    story.append(tabla_notas)
    story.append(Spacer(0, 5))
    des_tabla_puntaje = "Tabla 1: Puntaje obtenido por dimension y grupo de evaluadores."
    story = agregar_parrafo(story, des_tabla_puntaje, styles['TableDefinition'], Spacer(0, 15))

    datos = [
        [Paragraph("Resultado Global", styles['SubTitle'])],
        ["Resultado Final", Paragraph('{}'.format(resultado_persona.nota), styles['SubTitle'])]
    ]
    tabla_notaf = Table(datos, colWidths=[390, 70])
    tabla_notaf.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.aliceblue),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ('SPAN', (0, 0), (-1, 0)),
    ]))
    story.append(tabla_notaf)
    story.append(Spacer(0, 10))

    nivel_alcanzado = "El resultado global obtenido corresponde a un <b>{}</b> esto lo categoriza en el grupo <b>{}</b>.".format(
        resultado_persona.nota,
        resultado_persona.get_nivel
    )
    story = agregar_parrafo(story, nivel_alcanzado, styles['MyNormal'], PageBreak())

    # enc_tabla2 = "En la tabla 2 encontramos los promedios obtenidos por grupos de evaluadores en cada una de las áreas que aborda la encuesta."
    # story = agregar_parrafo(story, enc_tabla2, styles['MyNormal'], Spacer(0, 10))
    # datos = [primera_fila]
    # for n in notas:
    #     linea = [
    #         '{}'.format(n['pregunta__categoria__nombre']),
    #         Paragraph('{}'.format(floatformat(n['promedio_directivos']), 1), styles['SubTitle']),
    #         Paragraph('{}'.format(floatformat(n['promedio_pares']), 1), styles['SubTitle']),
    #         Paragraph('{}'.format(floatformat(n['promedio_autoevaluacion']), 1), styles['SubTitle']),
    #         Paragraph('{}'.format(floatformat(n['nota']), 1), styles['SubTitle'])
    #     ]
    #     datos.append(linea)
    # tabla_prom = Table(datos, colWidths=[200, 70, 50, 90, 50])
    # tabla_prom.setStyle(estilo_tabla)
    # story.append(tabla_prom)
    # story.append(Spacer(0, 5))
    # des_tabla2 = "Tabla 2: Resultados ponderados por área por evaluadores."
    # story = agregar_parrafo(story, des_tabla2, styles['TableDefinition'], Spacer(0, 30))

    enc_tabla3 = "La tabla 2 contiene los 3 ítems en los cuales obtuvo una menor puntuación desde la mirada de los <b>directivos</b>."
    des_tabla3 = "Tabla 2: Preguntas con menor puntuación de directivos."
    story = inicia_tabla_preguntas(
        story,
        enc_tabla3,
        resultado_persona.resultadopreguntapersona_set.all().order_by('promedio_directivos')[:3],
        "EN0003",
        des_tabla3
    )

    enc_tabla4 = "La tabla 3 contiene los 3 ítems en los cuales obtuvo una menor puntuación desde la mirada de los <b>pares</b>."
    des_tabla4 = "Tabla 3: Preguntas con menor puntuación de pares."
    story = inicia_tabla_preguntas(
        story,
        enc_tabla4,
        resultado_persona.resultadopreguntapersona_set.all().order_by('promedio_pares')[:3],
        "EN0001",
        des_tabla4
    )

    enc_tabla5 = "La tabla 4 contiene los 3 ítems en los cuales obtuvo una menor puntuación desde la mirada de la <b>autoevaluación</b>."
    des_tabla5 = "Tabla 4: Preguntas con menor puntuación en autoevaluación."
    story = inicia_tabla_preguntas(
        story,
        enc_tabla5,
        resultado_persona.resultadopreguntapersona_set.all().order_by('promedio_autoevaluacion')[:3],
        "EN0000",
        des_tabla5
    )

    enc_tabla6 = "La tabla 5 contiene los 3 ítems en los cuales obtuvo una mayor puntuación desde la mirada de los <b>directivos</b>."
    des_tabla6 = "Tabla 5: Preguntas con menor puntuación de directivos."
    story = inicia_tabla_preguntas(
        story,
        enc_tabla6,
        resultado_persona.resultadopreguntapersona_set.all().order_by('-promedio_directivos')[:3],
        "EN0003",
        des_tabla6
    )

    enc_tabla7 = "La tabla 6 contiene los 3 ítems en los cuales obtuvo una mayor puntuación desde la mirada de los <b>pares</b>."
    des_tabla7 = "Tabla 6: Preguntas con menor puntuación de pares."
    story = inicia_tabla_preguntas(
        story,
        enc_tabla7,
        resultado_persona.resultadopreguntapersona_set.all().order_by('-promedio_pares')[:3],
        "EN0001",
        des_tabla7
    )

    enc_tabla8 = "La tabla 7 contiene los 3 ítems en los cuales obtuvo una mayor puntuación desde la mirada de la <b>autoevaluación</b>."
    des_tabla8 = "Tabla 7: Preguntas con menor puntuación en autoevaluación."
    story = inicia_tabla_preguntas(
        story,
        enc_tabla8,
        resultado_persona.resultadopreguntapersona_set.all().order_by('-promedio_autoevaluacion')[:3],
        "EN0000",
        des_tabla8
    )

    # last_line = "En el sitio www.evaluaciondocentesea.cl  ud. puede además de bajar este informe," \
    #             " consultar el resultado completo de las evaluaciones hechas por su equipo directivo hacia su desempeño durante este año."
    # story = agregar_parrafo(story, last_line, styles['MyNormal'], Spacer(0, 50))

    story = agregar_parrafo(story, "<b>Toma de Conocimiento</b>", styles['SubTitle'], Spacer(0, 30))
    tbl_data = [
        [Paragraph("........................................", styles["SubTitle"]),
         Paragraph("........................................", styles['SubTitle'])],
        [Paragraph("Director", styles["SubTitle"]), Paragraph("Docente", styles['SubTitle'])],
    ]
    tbl = Table(tbl_data)
    story.append(tbl)
    story.append(Spacer(0, 20))

    # story = agregar_parrafo(
    #     story,
    #     "Atentamente Agencia de Acompañamiento a la Gestión Educativa.",
    #     styles['MyNormal'],
    #     Spacer(0, 30)
    # )

    return story


def get_image(path, height=1*cm):
    img = utils.ImageReader(path)
    iw, ih = img.getSize()
    aspect = iw / float(ih)
    return Image(path, width=(height * aspect), height=height)


def header(canbass, doc):
    canbass.saveState()
    content = Paragraph("Sistema de Evaluación del Desempeño Profesional Docente", styles['Header'])
    w, h = content.wrap(doc.width, doc.topMargin)
    content.drawOn(canbass, doc.leftMargin, doc.height + doc.topMargin + (h*2))

    logo_ea = get_image(os.path.join(PATH_FILE, 'static/base/img/logoEApdf.png'), height=40)
    w, h = logo_ea.wrap(doc.width, doc.topMargin)
    logo_ea.drawOn(canbass, doc.leftMargin, doc.height + doc.topMargin + (h/2))

    logo_aage = get_image(os.path.join(PATH_FILE, 'static/base/img/logoAAGEpdf.png'), height=40)
    w, h = logo_aage.wrap(doc.width, doc.topMargin)
    logo_aage.drawOn(canbass, doc.width, doc.height + doc.topMargin + (h/2))
    canbass.restoreState()


def inicia_tabla_preguntas(story, enc, queryset, tipo_encuesta, des_tabla):
    story = agregar_parrafo(story, enc, styles['MyNormal'], Spacer(0, 10))
    datos = [[
        Paragraph("Dimensiones", styles['SubTitle']),
        Paragraph("Nro.", styles['SubTitle']),
        Paragraph("Pregunta", styles['SubTitle']),
        Paragraph("Nota", styles['SubTitle']),
    ]]
    for p in queryset:
        if tipo_encuesta == "EN0003":
            promedio = p.promedio_directivos
        elif tipo_encuesta == "EN0001":
            promedio = p.promedio_pares
        else:
            promedio = p.promedio_autoevaluacion

        linea = [
            '{}'.format(p.pregunta.categoria.nombre),
            Paragraph('{}'.format(p.pregunta.numero_pregunta), styles['SubTitle']),
            '{}'.format(p.pregunta.pregunta),
            Paragraph('{}'.format(floatformat(promedio), 1), styles['SubTitle']),
        ]
        datos.append(linea)
    tabla = Table(datos, colWidths=[120, 40, 260, 40])
    tabla.setStyle(estilo_tabla)
    story.append(tabla)
    story.append(Spacer(0, 5))
    story = agregar_parrafo(story, des_tabla, styles['TableDefinition'], Spacer(0, 30))
    return story


def base_pdf(buffer):
    pdf = SimpleDocTemplate(
        buffer if buffer else 'Visualización resultados EVADO.pdf',
        pagesize=letter
    )
    frame = Frame(pdf.leftMargin, pdf.bottomMargin, pdf.width, pdf.height, id='normal')

    pdf.addPageTemplates([
        PageTemplate(id='contenido', frames=frame, onPage=header)
    ])

    story = []
    return {'story': story, 'pdf': pdf}


def pdf_response(resultado_persona):
    buffer = BytesIO()
    base = base_pdf(buffer)
    story = generar_pdf_resultados(resultado_persona, base['story'])
    base['pdf'].build(story, onLaterPages=header)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Reporte Evaluación Docente - {}.pdf"'.format(resultado_persona.persona)
    response.write(buffer.getvalue())
    buffer.close()

    return response


def multi_pdf_response(resultados_persona, colegio):
    buffer = BytesIO()
    base = base_pdf(buffer)
    story = base['story']
    for resultado_persona in resultados_persona:
        story = generar_pdf_resultados(resultado_persona, story)
        story.append(PageBreak())
    base['pdf'].build(story, onLaterPages=header)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Reportes Evaluación Docente - {}.pdf"'.format(colegio)
    response.write(buffer.getvalue())
    buffer.close()

    return response
