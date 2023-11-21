import csv
import io
import tempfile
from datetime import datetime
import base64
import matplotlib.pyplot as plt
import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side
from openpyxl.drawing.image import Image
from django.shortcuts import render, get_object_or_404
from jinja2 import FileSystemLoader, Environment
import plotly.graph_objects as go
from reportlab.lib.pagesizes import letter

from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Image, Paragraph
from django.template.loader import get_template
from django.template import Context
from django.conf import settings
from jinja2 import Environment, FileSystemLoader
import tempfile
import pdfkit
from Modelos.models import *
from django.http import JsonResponse, HttpResponse
from django.db.models import Count
from xhtml2pdf import pisa


from Secretaria.views.reports import generar_grafico


# Página del Tablero
def pageTablero(request):
    cant_estudiantes = Estudiante.objects.count()
    genero_count = (
        Estudiante.objects.values("genero__nombre")
        .annotate(total=Count("genero"))
        .order_by("genero__nombre")
    )

    for item in genero_count:
        print(f'Género: {item["genero__nombre"]}, Total: {item["total"]}')
    cant_docentes = Docente.objects.count()
    year_actual = datetime.now().year
    anolectivo = (
        Periodo.objects.values_list("nombre", flat=True)
        .filter(nombre=year_actual)
        .first()
    )

    return render(
        request,
        "tablero.html",
        {
            "cant_estudiantes": cant_estudiantes,
            "cant_docentes": cant_docentes,
            "anolectivo": anolectivo,
        },
    )


# Página de Estudiantes
def pageEstudiantes(request):
    if request.method == "GET":
        # estudiantes = Estudiante.objects.filter(eliminado = False)[:50]
        cant_estudiantes = Estudiante.objects.all().count()
        return render(
            request,
            "estudiantes/estdnt_listar.html",
            {
                # "estudiantes": estudiantes,
                "cant_estudiantes": cant_estudiantes,
            },
        )
    else:
        mensaje = "Este método sólo soporta una petición GET"
        print(mensaje)
        return JsonResponse({"resultado": mensaje})


def pageEstudiantes2(request):
    if request.method == "GET":
        # estudiantes = Estudiante.objects.filter(eliminado = False)[:50]
        cant_estudiantes2 = Estudiante.objects.all().count()
        return render(
            request,
            "tablero.html",
            {
                # "estudiantes": estudiantes,
                "cant_estudiantes2": cant_estudiantes2,
            },
        )
    else:
        mensaje = "Este método sólo soporta una petición GET"
        print(mensaje)
        return JsonResponse({"resultado": mensaje})


def pageAgregarEstudiante(request):
    if request.method == "GET":
        paises = Pais.objects.all()
        generos = Genero.objects.all()
        estados_civiles = EstadoCivil.objects.all()
        discapacidades = Discapacidad.objects.all()
        etnias = Etnia.objects.all()
        provincias = Provincia.objects.all()
        ciudades = Ciudad.objects.filter(
            provincia_id=13
        )  # Cantones de la provincia de Los Ríos

        modalidad_estudios = ModalidadEstudio.objects.all()
        jornadas = Jornada.objects.all()
        numeroMatriculas = NumeroMatricula.objects.all()

        grados = Grado.objects.all()
        niveles = Nivel.objects.all()
        paralelos = Paralelo.objects.all()
        especialidades = Especialidad.objects.all()
        periodos = Periodo.objects.order_by("-id")
        estados = Estado.objects.all()

        tipos_anexos = TiposAnexo.objects.all()

        return render(
            request,
            "estudiantes/estdnt_agregar.html",
            {
                "paises": paises,
                "generos": generos,
                "estados_civiles": estados_civiles,
                "discapacidades": discapacidades,
                "etnias": etnias,
                "provincias": provincias,
                "ciudades": ciudades,
                "modalidad_estudios": modalidad_estudios,
                "jornadas": jornadas,
                "numeroMatriculas": numeroMatriculas,
                "grados": grados,
                "niveles": niveles,
                "paralelos": paralelos,
                "especialidades": especialidades,
                "periodos": periodos,
                "estados": estados,
                "tipos_anexos": tipos_anexos,
            },
        )
    else:
        mensaje = "Este método sólo soporta una petición GET"
        print(mensaje)
        return JsonResponse({"resultado": mensaje})


def pageEditarEstudiante(request, id_estudiante):
    if request.method == "GET":
        estudiante = Estudiante.objects.get(pk=int(id_estudiante))
        paises = Pais.objects.all()
        generos = Genero.objects.all()
        estados_civiles = EstadoCivil.objects.all()
        discapacidades = Discapacidad.objects.all()
        provincias = Provincia.objects.all()
        ciudades = Ciudad.objects.filter(provincia_id=estudiante.provincia.id)

        modalidad_estudios = list(ModalidadEstudio.objects.all().values())
        jornadas = list(Jornada.objects.all().values())
        numeroMatriculas = list(NumeroMatricula.objects.all().values())

        grados = list(Grado.objects.all().values())
        niveles = list(Nivel.objects.all().values())
        paralelos = list(Paralelo.objects.all().values())
        especialidades = list(Especialidad.objects.all().values())
        periodos = list(Periodo.objects.order_by("-id").values())
        estados = list(Estado.objects.all().values())

        tipos_anexos = list(TiposAnexo.objects.all().values())

        return render(
            request,
            "estudiantes/estdnt_editar.html",
            {
                "estudiante": estudiante,
                "paises": paises,
                "generos": generos,
                "estados_civiles": estados_civiles,
                "discapacidades": discapacidades,
                "provincias": provincias,
                "ciudades": ciudades,
                "modalidad_estudios": modalidad_estudios,
                "jornadas": jornadas,
                "numeroMatriculas": numeroMatriculas,
                "grados": grados,
                "niveles": niveles,
                "paralelos": paralelos,
                "especialidades": especialidades,
                "periodos": periodos,
                "estados": estados,
                "tipos_anexos": tipos_anexos,
            },
        )
    else:
        print("Este método sólo soporta una petición POST")


# Página Docentes
def pageDocentes(request):
    if request.method == "GET":
        # estudiantes = Docente.objects.filter(eliminado = False)[:50]
        cant_docentes = Docente.objects.all().count()
        return render(
            request,
            "docentes/docnt_listar.html",
            {
                # "estudiantes": estudiantes,
                "cant_docentes": cant_docentes,
            },
        )
    else:
        mensaje = "Este método sólo soporta una petición GET"
        print(mensaje)
        return JsonResponse({"resultado": mensaje})


def pageAgregarDocente(request):
    if request.method == "GET":
       etnias = Etnia.objects.all()

       return render(request, "docentes/docnt_agregar.html", {"etnias": etnias})
    else:
        mensaje = "Este método sólo soporta una petición GET"
        print(mensaje)
        return JsonResponse({"resultado": mensaje})


def pageEditarDocente(request, id_docente):
    if request.method == "GET":
        docente = Docente.objects.get(pk=int(id_docente))

        return render(
            request,
            "docentes/docnt_editar.html",
            {
                "docente": docente,
                #"paises": paises,
                #"generos": generos,
                #"estados_civiles": estados_civiles,
                #"discapacidades": discapacidades,
                #"provincias": provincias,
                #"ciudades": ciudades,
            },
        )
    else:
        print("Este método sólo soporta una petición POST")


# Página Autoridades
def pageAutoridades(request):
    return render(request, "autoridades/autoridades.html")


# Página Institución
def pageInstitucionAbout(request):
    return render(request, "institucion/institucion-sobre-nosotros.html")


def pageInstitucionContacto(request):
    return render(request, "institucion/institucion-contacto.html")


def pageInstitucionBlogs(request):
    return render(request, "institucion/institucion-blogs.html")


# Página Reportes


def generar_pdf_estudiante(request):
    estudiantes = Estudiante.objects.all()
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="estudiantes.pdf"'
    buffer = io.BytesIO()
    p = SimpleDocTemplate(buffer, pagesize=letter)
    elementos = []
    data = [
        ["#", "Nombres", "Apellidos", "Correo", "Direccion", "Celular", "Provincia"]
    ]
    for idx, estudiante in enumerate(estudiantes, start=1):
        data.append(
            [
                str(idx),
                estudiante.nombres,
                estudiante.apellidos,
                estudiante.correo,
                estudiante.direccion,
                estudiante.celular,
                estudiante.provincia.nombre,
            ]
        )

    # Estilos de la tabla
    style = TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), "#CCCCCC"),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), "#EEEEEE"),
            ("GRID", (0, 0), (-1, -1), 0.5, "#000000"),
        ]
    )

    table = Table(data)
    table.setStyle(style)
    elementos.append(table)
    p.build(elementos)
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


def generar_reporte_excel_estudiante(request):
    estudiantes = Estudiante.objects.all()

    # Crear un nuevo libro de trabajo y hoja de trabajo
    wb = openpyxl.Workbook()
    ws = wb.active

    # Definir estilos
    header_font = Font(bold=True)
    header_alignment = Alignment(horizontal="center")
    cell_border = Border(left=Side(style="thin"), right=Side(style="thin"), top=Side(style="thin"),
                         bottom=Side(style="thin"))

    # Agregar encabezados con estilo
    ws.append(["#", "Nombres", "Apellidos", "Correo", "Dirección", "Celular", "Provincia"])
    header_row = ws[1]
    for cell in header_row:
        cell.font = header_font
        cell.alignment = header_alignment
        cell.border = cell_border

    # Llenar los datos de los estudiantes
    for idx, estudiante in enumerate(estudiantes, start=1):
        ws.append(
            [idx, estudiante.nombres, estudiante.apellidos, estudiante.correo, estudiante.direccion, estudiante.celular,
             estudiante.provincia.nombre])

    # Configurar ancho de columna automático
    for column in ws.columns:
        max_length = 0
        column = [cell for cell in column]
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass
        adjusted_width = (max_length + 2)
        ws.column_dimensions[column[0].column_letter].width = adjusted_width

    # Crear una respuesta HTTP con el archivo Excel
    response = HttpResponse(content_type="application/vnd.ms-excel")
    response["Content-Disposition"] = 'attachment; filename="estudiantes.xlsx"'
    wb.save(response)
    return response


def generar_reporte_csv_estudiante(request):
    estudiantes = Estudiante.objects.all()
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="estudiantes.csv"'
    writer = csv.writer(response)
    writer.writerow(
        ["#", "Nombres", "Apellidos", "Correo", "Direccion", "Celular", "Provincia"]
    )
    for idx, estudiante in enumerate(estudiantes, start=1):
        writer.writerow(
            [
                str(idx),
                estudiante.nombres,
                estudiante.apellidos,
                estudiante.correo,
                estudiante.direccion,
                estudiante.celular,
                estudiante.provincia.nombre,
            ]
        )
    return response


##creaunafuncionquegenereunpdfapartirdelidqueseseleccione,sedebeimprimirlainformaciondelestudiante
def generar_pdf_estudiante_x_estudiante(request, id_estudiante):
    try:
        estudiante = Estudiante.objects.get(pk=id_estudiante)
    except Estudiante.DoesNotExist:
        return HttpResponse("Estudiante no encontrado", status=404)

        # Obtener el año actual
    year = datetime.now().year

    # Obtener la ruta del template
    template_path = (
        "estudiantes/pdf_template.html"  # Reemplaza con la ruta de tu template
    )

    # Cargar el template
    template = get_template(template_path)

    # Renderizar el template con los datos del estudiante
    context = {
        "estudiante": estudiante,
        "year": year,
        "image_path": "static/img/uem-logo-100.png",
    }
    html = template.render(context)

    # Crear el archivo PDF
    pdf_file = tempfile.NamedTemporaryFile(delete=False)
    pdf_file.close()

    # Generar el PDF a partir del HTML
    with open(pdf_file.name, "wb") as f:
        pisa.CreatePDF(html, dest=f)

    # Descargar el archivo PDF
    with open(pdf_file.name, "rb") as f:
        response = HttpResponse(f.read(), content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="estudiante.pdf"'

    return response


def pageReportesEstudiantes(request):
    """
  
  """ """  anolectivo = Periodo.objects.all()
    list_anos = []
    for ano in anolectivo:
        list_anos.append({
            'id': ano.id,
            'nombre': int(ano.nombre),
            'nombre2': int(ano.nombre) + 1 ,
            
        })

    print("Veamos que sale")
    print(list_anos)
    anio = request.POST.get('anio')
    graph = generar_grafico(anio)
    return render(request, 'reportes/reportes-estudiantes.html',{
        'list_anos': reversed(list_anos), 'graph': graph,
     })"""
    """
  select_year = request.GET.get('select_id_year')
  select_year_query = request.GET.get('select_id_year_query')
  if select_year:
      year_studiante = Estudiante.objects.filter(curso__periodo__nombre = select_year)
      genero_counts = year_studiante.values('genero__nombre').annotate(count=Count('genero'))
  else:
      genero_counts = Estudiante.objects.values('genero__nombre').annotate(count=Count('genero'))
  labels = []
  counts = []

  for genero_count in genero_counts:
      labels.append(genero_count['genero__nombre'])
      counts.append(genero_count['count'])

  #crear un figura con dimensiones personalizadas
  plt.figure(figsize=(2,2))

  #generar el grafico
  plt.bar(labels, counts)
  plt.xlabel('Genero')
  plt.ylabel('Cantidad Estudiantes')
  plt.title(f'Distribución de Estudiantes por Genero - Año {select_year}')

  #convertir el grafico a una imagen en formato base64
  image_stream = io.BytesIO()
  plt.savefig(image_stream, format='png')
  plt.close()
  image_base64 = base64.b64encode(image_stream.getvalue()).decode('utf-8')

  #obtener los años disponibles para el menu desplegable
  available_year = Periodo.objects.values_list('nombre', flat=True)
  context =  {
      'image_base64': image_base64,
      'available_year': available_year,
      'select_year': select_year,
  }
  return render(request, 'reportes/reportes-estudiantes.html', context)
  """
    available_year = Periodo.objects.values_list("nombre", flat=True)
    # generar funcion que muestre un tabla de datos, segun datos seleccionados
    select_periordo = request.GET.get("periodo")
    select_genero_masculino = request.GET.get("Masculino")
    select_genero_femenino = request.GET.get("Femenino")
    select_genero_intersexual = request.GET.get("Intersexual")
    select_discapacidad_si = request.GET.get("Si")
    select_discapacidad_no = request.GET.get("No")
    select_estado_casado = request.GET.get("Casado")
    select_estado_soltero = request.GET.get("Soltero")
    select_estado_anulado = request.GET.get("Anulado")
    select_estado_separado = request.GET.get("Separado")
    select_estado_viudo = request.GET.get("Viudo")
    select_estado_unionLibre = request.GET.get("Unio Libre")
    select_etnia_Montubio = request.GET.get("Montubio")
    select_etnia_Mestizo = request.GET.get("Mestizo")
    select_etnia_Afroecuatoriano = request.GET.get("Afroecuatoriano")
    select_etnia_Indigena = request.GET.get("Indigena")
    select_etnia_Blanco = request.GET.get("Blanco")

    seleccion_genero = any(
        [select_genero_masculino, select_genero_femenino, select_genero_intersexual]
    )
    seleccion_discapacidad = any([select_discapacidad_si, select_discapacidad_no])
    seleccion_estadoCivil = any(
        [
            select_estado_anulado,
            select_estado_unionLibre,
            select_estado_casado,
            select_estado_soltero,
            select_estado_separado,
            select_estado_viudo,
        ]
    )
    seleccion_etnia = any(
        [
            select_etnia_Afroecuatoriano,
            select_etnia_Indigena,
            select_etnia_Blanco,
            select_etnia_Mestizo,
            select_etnia_Montubio,
        ]
    )

    if (
        seleccion_discapacidad
        or seleccion_etnia
        or seleccion_genero
        or seleccion_estadoCivil
    ):
        estudiante = Estudiante.objects.filter(
            periodo__nombre=select_periordo,
            genero__nombre=seleccion_genero,
            etnia__nombre=seleccion_etnia,
            discacidad__nombre=seleccion_discapacidad,
            estadocivil__nombre=seleccion_estadoCivil,
        )
    else:
        estudiante = Estudiante.objects.all()

    context = {
        "estudiantes_query": estudiante,
        "seleccion_genero": seleccion_genero,
        "seleccion_discapacidad": seleccion_discapacidad,
        "seleccion_etnia": seleccion_etnia,
        "seleccion_estadoCivil": seleccion_estadoCivil,
        "available_year": available_year,
        "select_year": available_year,
    }



    select_anio = request.GET.get("select_id_year")
    print(select_anio)
    print(context)
    return render(request, "reportes/reportes-estudiantes.html", context)


def generar_grafico_barras(request):
    select_year = request.GET.get("anio")
    generos = Genero.objects.all()
    labels = [genero.nombre for genero in generos]
    cantidad_estudiantes = []

    for genero in generos:
        cantidad = Estudiante.objects.filter(
            genero=genero
        ).aggregate(  # Filtrar por género
            total=Count("id")
        )  # Contar estudiantes por género

        cantidad_estudiantes.append(cantidad["total"])  # Agregar la cantidad a la lista

    data = {
        "labels": labels,
        "cantidad_estudiantes": cantidad_estudiantes,
    }
    print(cantidad_estudiantes)
    return JsonResponse(data)


def generar_grafico_estado_estudiantes(request):
    estados = Estado.objects.all()
    labels = [estado.nombre for estado in estados]
    cantidad_x_estado = []

    for estado in estados:
        cantidad = Curso.objects.filter(estado=estado).aggregate(total=Count("id"))
        cantidad_x_estado.append(cantidad["total"])

    total_estudiantes_x_estado = sum(cantidad_x_estado)
    porcentaje = [
        cantidad * 100 / total_estudiantes_x_estado
        if total_estudiantes_x_estado > 0
        else 0
        for cantidad in cantidad_x_estado
    ]

    data = {"labels": labels, "porcentaje": porcentaje}
    print(cantidad_x_estado)
    return JsonResponse(data)


def mostrar_reporte_tabla(request):
    # generar funcion que muestre un tabla de datos, segun datos seleccionados
    select_periordo = request.GET.get("periodo")
    select_genero_masculino = request.GET.get("Masculino")
    select_genero_femenino = request.GET.get("Femenino")
    select_genero_intersexual = request.GET.get("Intersexual")
    select_discapacidad_si = request.GET.get("Si")
    select_discapacidad_no = request.GET.get("No")
    select_estado_casado = request.GET.get("Casado")
    select_estado_soltero = request.GET.get("Soltero")
    select_estado_anulado = request.GET.get("Anulado")
    select_estado_separado = request.GET.get("Separado")
    select_estado_viudo = request.GET.get("Viudo")
    select_estado_unionLibre = request.GET.get("Unio Libre")
    select_etnia_Montubio = request.GET.get("Montubio")
    select_etnia_Mestizo = request.GET.get("Mestizo")
    select_etnia_Afroecuatoriano = request.GET.get("Afroecuatoriano")
    select_etnia_Indigena = request.GET.get("Indigena")
    select_etnia_Blanco = request.GET.get("Blanco")

    seleccion_genero = any(
        [select_genero_masculino, select_genero_femenino, select_genero_intersexual]
    )
    seleccion_discapacidad = any([select_discapacidad_si, select_discapacidad_no])
    seleccion_estadoCivil = any(
        [
            select_estado_anulado,
            select_estado_unionLibre,
            select_estado_casado,
            select_estado_soltero,
            select_estado_separado,
            select_estado_viudo,
        ]
    )
    seleccion_etnia = any(
        [
            select_etnia_Afroecuatoriano,
            select_etnia_Indigena,
            select_etnia_Blanco,
            select_etnia_Mestizo,
            select_etnia_Montubio,
        ]
    )

    if (
        seleccion_discapacidad
        or seleccion_etnia
        or seleccion_genero
        or seleccion_estadoCivil
    ):
        estudiante = Estudiante.objects.filter(
            periodo__nombre=select_periordo,
            genero__nombre=seleccion_genero,
            etnia__nombre=seleccion_etnia,
            discacidad__nombre=seleccion_discapacidad,
            estadocivil__nombre=seleccion_estadoCivil,
        )
    else:
        estudiante = Estudiante.objects.all()

    context = {
        "estudiantes": estudiante,
        "seleccion_genero": seleccion_genero,
        "seleccion_discapacidad": seleccion_discapacidad,
        "seleccion_etnia": seleccion_etnia,
        "seleccion_estadoCivil": seleccion_estadoCivil,
    }

    return render(request)


def pageReportesDocentes(request):
    return render(request, "reportes/reportes-docentes.html")


def pageReportesAutoridades(request):
    return render(request, "reportes/reportes-autoridades.html")


# Página Manual de usuario
def pageManualDeusuario(request):
    return render(request, "manual-usuario/manual-usuario.html")


# Página Patrocinadores
def pagePatrocinadores(request):
    return render(request, "patrocinadores/patrocinadores.html")


# Página Perfil
def pagePerfil(request):
    return render(request, "perfil/perfil.html")


# Página Configuracion
def pageConfiguracion(request):
    return render(request, "configuracion/configuracion.html")
