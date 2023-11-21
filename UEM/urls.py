from django.contrib import admin
from django.urls import path

from Inicio.views import sitio_web
from Inicio.views import autenticacion

from Secretaria.views import estudiantes_api_rest as sctr_estudiantes
from Secretaria.views import docentes_api_rest as sctr_docentes
from Secretaria.views import docenteApiRest as sctr_docentes2
from Secretaria.views import pages as sctr_pages
from Secretaria.views import reports as sctr_report

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    # SITIO WEB
    path("", sitio_web.pageIndex, name="home"),
    path("about/", sitio_web.pageSobreNosotros, name="about"),
    path("contacto/", sitio_web.pageContacto, name="contacto"),
    path("blog/", sitio_web.pageBlogs, name="blog"),
    # FIN SECCIÓN SITIO WEB
    # SECCIÓN INICIO
    # Login
    path("login/", autenticacion.pageLogin, name="login"),
    path("autenticar/", autenticacion.getJsonIniciarSesion),
    # Recuperar contraseña
    path(
        "recuperar-password/",
        autenticacion.pageRecuperarPassword,
        name="recuperar-password",
    ),
    path("verificar-correo/", autenticacion.getJsonVerificarCorreo),
    path("enviar-password-x-correo/", autenticacion.getJsonEnviarPasswordXCorreo),
    # Cerrar sesión
    path("cerrar-sesion/", autenticacion.cerrarSesion, name="cerrar-sesion"),
    # FIN SECCIÓN INICIO
    # SECCIÓN SECRETARÍA
    # Menú
    path("tablero-secretaria/", sctr_pages.pageTablero, name="tablero-secretaria"),
    path(
        "estudiantes-secretaria/",
        sctr_pages.pageEstudiantes,
        name="estudiantes-secretaria",
    ),
    path("docentes-secretaria/", sctr_pages.pageDocentes, name="docentes-secretaria"),
    path(
        "autoriades-secretaria/",
        sctr_pages.pageAutoridades,
        name="autoridades-secretaria",
    ),
    path(
        "institucion-about-secretaria/",
        sctr_pages.pageInstitucionAbout,
        name="institucion-about-secretaria",
    ),
    path(
        "institucion-contacto-secretaria/",
        sctr_pages.pageInstitucionContacto,
        name="institucion-contacto-secretaria",
    ),
    path(
        "institucion-blogs-secretaria/",
        sctr_pages.pageInstitucionBlogs,
        name="institucion-blogs-secretaria",
    ),
    path(
        "reportes-x-estudiante-secretaria/",
        sctr_pages.pageReportesEstudiantes,
        name="reportes-x-estudiantes-secretaria",
    ),
    path(
        "generar_pdf_estudiante_x_estudiante/<int:id_estudiante>/",
        sctr_pages.generar_pdf_estudiante_x_estudiante,
        name="generar_pdf_estudiante",
    ),
    path(
        "generar-grafico/",
        sctr_pages.generar_grafico_barras,
        name="generar_grafico_anio",
    ),
    path(
        "generar-grafico-x-estado/",
        sctr_pages.generar_grafico_estado_estudiantes,
        name="graficos_estados_estudiantes",
    ),
    path(
        "generar-pdf/",
        sctr_pages.generar_pdf_estudiante,
        name="reportes-pdf-estudiante",
    ),
    path(
        "generar-excel/",
        sctr_pages.generar_reporte_excel_estudiante,
        name="reportes-excel-estudiante",
    ),
    path(
        "generar-csv/",
        sctr_pages.generar_reporte_csv_estudiante,
        name="reportes-csv-estudiante",
    ),
    path(
        "reportes-x-docentes-secretaria/",
        sctr_pages.pageReportesDocentes,
        name="reportes-x-docentes-secretaria",
    ),
    path(
        "reportes-x-autoridades-secretaria/",
        sctr_pages.pageReportesAutoridades,
        name="reportes-x-autoridades-secretaria",
    ),
    path("manual-usuario/", sctr_pages.pageManualDeusuario, name="manual-usuario"),
    path("patrocinadores/", sctr_pages.pagePatrocinadores, name="patrocinadores"),
    path("perfil/", sctr_pages.pagePerfil, name="perfil"),
    path(
        "configuración-cuenta/",
        sctr_pages.pageConfiguracion,
        name="configuracion-cuenta",
    ),
    # Menú Estudiantes
    path(
        "agregar-estudiante/",
        sctr_pages.pageAgregarEstudiante,
        name="agregar-estudiante",
    ),
    path(
        "editar-estudiante/<int:id_estudiante>",
        sctr_pages.pageEditarEstudiante,
        name="editar-estudiante",
    ),
    # Menú Docentes
    path("agregar-docente/", sctr_pages.pageAgregarDocente, name="agregar-docente"),
    path("editar-docente/<int:id_docente>", sctr_pages.pageEditarDocente, name="editar-docente"),
    # General
    path(
        "est-get-info-adicional/<int:id_estudiante>",
        sctr_estudiantes.getJSONInformacionAdicional,
    ),
    path("est-verificar-existe/", sctr_estudiantes.getJsonVerificarExisteEstudiante),
    path("doc-verificar-existe/", sctr_docentes2.verificarCedulaDocente),
    path(
        "obtener-ciudades-x-provincia/<int:id_provincia>",
        sctr_estudiantes.getJsonCiudadesXProvincia,
    ),
    
   # path(
    #    "obtener-ciudades-x-provincia/<int:id_provincia>",
    #    sctr_docentes.getJsonCiudadesXProvincia,
    #),
    # ESTUDIANTES
    path("buscar-estudiante/", sctr_estudiantes.getJsonBuscarEstudiante),
    path('busqueda-personalizada/',sctr_estudiantes.getJSONbuscarEstudianteQuery),
    path("obtener-estudiantes/", sctr_estudiantes.getJsonObtenerEstudiantes),
    # DOCENTES
    path("buscar-docente/", sctr_docentes2.getJsonBuscarDocente),
    path("obtener-docentes/", sctr_docentes2.getJsonObtenerDocentes),
    # Registro Estudiante
    path(
        "est-agg-info-general/",
        sctr_estudiantes.vwRegistrarInformacionGeneral,
        name="estudiante-agregar-info-general",
    ),
    path(
        "est-agg-foto-perfil/",
        sctr_estudiantes.vwRegistrarFotoPerfilEstudiante,
        name="estudiante-agregar-foto-perfil",
    ),
    path(
        "est-agg-info-academica/",
        sctr_estudiantes.vwRegistrarInformacionAcademica,
        name="estudiante-agregar-info-academica",
    ),
    path(
        "est-agg-info-curso/",
        sctr_estudiantes.vwRegistrarHistorialCurso,
        name="estudiante-agregar-info-curso",
    ),
    path(
        "est-agg-anexo/",
        sctr_estudiantes.vwRegistrarAnexo,
        name="estudiante-agregar-anexo",
    ),
    path(
        "est-agg-representante/",
        sctr_estudiantes.vwRegistrarRepresentante,
        name="estudiante-agregar-representante",
    ),
    # Registro Docente
    path("doc-agg-info-general-docente/", sctr_docentes2.vwRegistrarDocente, name="docente-agregar-info-general-docente"),
    #foto de perfil
    path("doc-agg-foto-perfil-docente/", sctr_docentes2.vwRegistrarFotoPerfilDocente, name="docente-agregar-foto-perfil-docente"),
    # Edición
    path(
        "est-editar-info-general/",
        sctr_estudiantes.vwEditarInformacionGeneral,
        name="estudiante-editar-info-general",
    ),
    path(
        "est-editar-foto-perfil/",
        sctr_estudiantes.vwEditarFotoEstudiante,
        name="estudiante-editar-foto",
    ),
    path(
        "est-editar-info-academica/",
        sctr_estudiantes.vwEditarInformacionAcademica,
        name="estudiante-editar-info-academica",
    ),
    path(
        "est-editar-info-curso/",
        sctr_estudiantes.vwEditarHistorialCurso,
        name="estudiante-editar-info-curso",
    ),
    path(
        "est-editar-representante/",
        sctr_estudiantes.vwEditarRepresentante,
        name="estudiante-editar-representante",
    ),
    # Edicion Docente
    path("doc-editar-info-general-docente/", sctr_docentes2.vwEditarDocente, name="docente-editar-info-general-docente"),
    #foto de perfil
    path("doc-editar-foto-perfil-docente/", sctr_docentes2.vwEditarFotoDocente, name="docente-editar-foto-perfil-docente"),
   
    # Eliminación
    path(
        "est-eli-estudiante/",
        sctr_estudiantes.vwEliminarEstudiante,
        name="estudiante-eliminar-estudiante",
    ),
    #eliminar docente
    path(
        "doc-eli-docente/",
        sctr_docentes2.vwEliminarDocente,
        name="docente-eliminar-docente",
    ),
    path(
        "est-eliminar-curso/",
        sctr_estudiantes.vwEliminarCurso,
        name="estudiante-eliminar-curso",
    ),
    path(
        "est-eli-anexo/",
        sctr_estudiantes.vwEliminarAnexo,
        name="estudiante-eliminar-anexo",
    ),
    # reportes
    path(
        "reporte-estudiantes/",
        sctr_estudiantes.generate_pdf_report_estudent,
        name="reporte-estudiantes",
    ),
    path('population-chart/', sctr_estudiantes.popultaion_chart, name='population-chart'),
    # FIN SECCION SECRETARIA
]

# Creando el acceso para los archivos de media
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
