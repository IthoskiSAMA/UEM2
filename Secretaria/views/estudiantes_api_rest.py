from django.db import transaction
from django.db.models import Sum

from Modelos.models import *
from django.views.decorators.csrf import requires_csrf_token
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse
import os
from datetime import datetime
from reportlab.pdfgen import canvas
from django.shortcuts import render

from Secretaria.views.pages import generar_grafico_barras


# OBTENER INFORMACIÓN ADICIONAL
def getJSONInformacionAdicional(request, id_estudiante):
    if request.method == "GET":
        try:
            unInformacionAcademica = list(
                InformacionAcademica.objects.filter(
                    estudiante_id=int(id_estudiante)
                ).values()
            )

            unosCursos = Curso.objects.filter(estudiante_id=int(id_estudiante))
            listaCursos = []
            for curso in unosCursos:
                listaCursos.append(
                    {
                        "especialidad": curso.especialidad.nombre,
                        "estado": curso.estado.nombre,
                        "estado_id": curso.estado.id,
                        "grado": curso.grado.nombre,
                        "curso_id": curso.id,
                        "nivel": curso.nivel.nombre,
                        "paralelo": curso.paralelo.nombre,
                        "periodo": curso.periodo.nombre,
                    }
                )

            unosAnexos = Anexos.objects.filter(estudiante_id=int(id_estudiante))
            listaAnexos = []
            for anexo in unosAnexos:
                listaAnexos.append(
                    {
                        "tipo_anexo_id": anexo.tipo_anexo.id,
                        "anexo_id": anexo.id,
                        "anexo_nombre": anexo.archivo.name.split("/")[-1],
                        "anexo_url": anexo.archivo.url,
                        "anexo_periodo": anexo.periodo.nombre,
                    }
                )

            unRepresentante = list(
                Representante.objects.filter(estudiante_id=int(id_estudiante)).values()
            )
            return JsonResponse(
                {
                    "resultado": 1,
                    "unInformacionAcademica": unInformacionAcademica,
                    "listaCursos": listaCursos,
                    "listaAnexos": listaAnexos,
                    "unRepresentante": unRepresentante,
                },
                safe=False,
            )
        except ObjectDoesNotExist:
            return JsonResponse({"resultado": 0})
    else:
        mensaje = "Este método sólo soporta una petición GET"
        print(mensaje)
        return JsonResponse({"resultado": mensaje})


# VERIFICAR SI LA CÉDULA YA ESTÁ REGISTRADA
@requires_csrf_token
def getJsonVerificarExisteEstudiante(request):
    if request.method == "POST":
        try:
            with transaction.atomic():
                existeEstudiante = Estudiante.objects.filter(
                    cedula=request.POST["cedula"]
                ).exists()
                if existeEstudiante == False:
                    return JsonResponse({"resultado": 1})
                else:
                    return JsonResponse({"resultado": 0})
        except Exception as ex:
            return JsonResponse({"resultado": -1})
    else:
        return JsonResponse({"resultado": "Este método sólo soporta una petición POST"})


# OBTENER CIUDADES POR PROVINCIA
def getJsonCiudadesXProvincia(request, id_provincia):
    if request.method == "GET":
        try:
            ciudades = list(Ciudad.objects.filter(provincia__id=id_provincia).values())
            return JsonResponse(ciudades, safe=False)
        except Exception as ex:
            print(ex)
            return JsonResponse({"resultado": ex})
    else:
        mensaje = "Este método sólo soporta petición GET"
        print(mensaje)
        return JsonResponse({"resultado": mensaje})


# BUSCAR ESTUDIANTE
def getJSONbuscarEstudianteQuery(request):
    if request.method == "POST":
        anio_query = request.POST.get("select_year_query")
        pais_ecuador_query = request.POST.get("ecuatoriano")
        pais_extrangero_query = request.POST.get("extrangero")
        provincia_lrios_query = request.POST.get("losrios")
        provincia_otras_query = request.POST.get("otrasprovincias")
        ciudad_quevedo_query = request.POST.get("quevedo")
        ciudad_otras_query = request.POST.get("otraciudad")
        etnia_montubio_query = request.POST.get("montubio")
        etnia_afroamericano_query = request.POST.get("afroamericano")
        etnia_indigena_query = request.POST.get("indigena")
        etnia_blanco_query = request.POST.get("blanco")
        masculino_query = request.POST.get("masculino")
        femenino_query = request.POST.get("femenino")
        intersexual_query = request.POST.get("intersexual")
        discapacidad_si_query = request.POST.get("discapacidad_si")
        discapacidad_no_query = request.POST.get("discapacidad_no")

        estudiantes_query = Estudiante.objects.filter(eliminado=False)

        if pais_ecuador_query:
            estudiantes_query = estudiantes_query.filter(pais__nombre="Ecuador (predeterminado)")

        if pais_extrangero_query:
            estudiantes_query = estudiantes_query.exclude(pais__nombre="Ecuador (predeterminado)")

        if provincia_lrios_query:
            estudiantes_query = estudiantes_query.filter(provincia__nombre="Los Ríos")

        if provincia_otras_query:
            estudiantes_query = estudiantes_query.exclude(provincia__nombre="Los Ríos")

        if ciudad_quevedo_query:
            estudiantes_query = estudiantes_query.filter(ciudad__nombre="Quevedo")

        if ciudad_otras_query:
            estudiantes_query = estudiantes_query.exclude(ciudad__nombre="Quevedo")

        if etnia_montubio_query:
            estudiantes_query = estudiantes_query.filter(etnia__nombre="Montubio")

        if etnia_afroamericano_query:
            estudiantes_query = estudiantes_query.filter(etnia__nombre="Afroecuatoriano")

        if etnia_indigena_query:
            estudiantes_query = estudiantes_query.filter(etnia__nombre="Indígena")

        if etnia_blanco_query:
            estudiantes_query = estudiantes_query.filter(etnia__nombre="Blanco")

        if masculino_query:
            estudiantes_query = estudiantes_query.filter(genero__nombre="Masculino")

        if femenino_query:
            estudiantes_query = estudiantes_query.filter(genero__nombre="Femenino")

        if intersexual_query:
            estudiantes_query = estudiantes_query.filter(genero__nombre="Intersexual")

        if discapacidad_si_query:
            estudiantes_query = estudiantes_query.filter(discapacidad__nombre="Si")

        if discapacidad_no_query:
            estudiantes_query = estudiantes_query.filter(discapacidad__nombre="No")

        estudiantes_query = estudiantes_query[:10].values()

        response_data = list(estudiantes_query)

        if not response_data:
            return JsonResponse({"resultado": 0})
        print(response_data)
        return JsonResponse({"resultado": 1, "listaEstudianteQuery": response_data})

    mensaje = "Este método solo soporta una petición POST"
    print(mensaje)
    return JsonResponse({"resultado": mensaje})

@requires_csrf_token
def getJsonBuscarEstudiante(request):
    if request.method == "POST":
        datos = request.POST["inputDatos"]
        response = None

        if request.POST["selecBuscar"] == "cedula":
            response = list(
                Estudiante.objects.filter(cedula__icontains=datos, eliminado=False)[
                    :50
                ].values()
            )

        elif request.POST["selecBuscar"] == "apellidos":
            response = list(
                Estudiante.objects.filter(apellidos__icontains=datos, eliminado=False)[
                    :50
                ].values()
            )

        elif request.POST["selecBuscar"] == "nombres":
            response = list(
                Estudiante.objects.filter(nombres__icontains=datos, eliminado=False)[
                    :50
                ].values()
            )

        else:
            return JsonResponse({"resultado": 0})

        if response == []:
            return JsonResponse({"resultado": 0})

        return JsonResponse({"resultado": 1, "listaEstudiantes": response})
    else:
        mensaje = "Este método sólo soporta una petición POST"
        print(mensaje)
        # 1 -> success
        # 0 -> fail
        # -1 -> error
        return JsonResponse({"resultado": mensaje})


# OBTENER LISTA DE ESTUDIANTES
def getJsonObtenerEstudiantes(request):
    if request.method == "GET":
        response = list(Estudiante.objects.filter(eliminado=False)[:100].values())
        if response == []:
            return JsonResponse({"resultado": 0})

        return JsonResponse({"resultado": 1, "listaEstudiantes": response})
    else:
        return JsonResponse({"resultado": "Este método sólo soporta una petición GET"})


# REGISTRAR INFORMACIÓN GENERAL
@requires_csrf_token
def vwRegistrarInformacionGeneral(request):
    if request.method == "POST":
        try:
            with transaction.atomic():
                # datos requeridos
                unEstudiante = Estudiante()
                unEstudiante.nombres = request.POST["inputNombres"]
                unEstudiante.apellidos = request.POST["inputApellidos"]
                unEstudiante.cedula = request.POST["inputCedula"]
                # fin datos requeridos

                # datos opcionales
                unEstudiante.pais = Pais.objects.get(
                    pk=int(request.POST["selecPaisOrigen"])
                )
                if request.POST.get("inputNacimiento", False) != "":
                    unEstudiante.fecha_nacimiento = request.POST.get(
                        "inputNacimiento", False
                    )
                if request.POST.get("inputCorreo", False) != "":
                    unEstudiante.correo = request.POST.get("inputCorreo", False)

                if request.POST.get("selecGenero", False) != "0":
                    genero = Genero.objects.get(
                        pk=request.POST.get("selecGenero", False)
                    )
                    unEstudiante.genero = genero
                if request.POST.get("selecEstadoCivil", False) != "0":
                    estado_civil = EstadoCivil.objects.get(
                        pk=request.POST.get("selecEstadoCivil", False)
                    )
                    unEstudiante.estado_civil = estado_civil
                if request.POST.get("selecDiscapacidad", False) != "0":
                    discapacidad = Discapacidad.objects.get(
                        pk=request.POST.get("selecDiscapacidad", False)
                    )
                    unEstudiante.discapacidad = discapacidad

                if request.POST.get("selecEtnia", False) != "0":
                    etnia = Etnia.objects.get(pk=request.POST.get("selecEtnia", False))
                    unEstudiante.etnia = etnia
                if request.POST.get("selecProvincia", False) != "0":
                    provincia = Provincia.objects.get(
                        pk=request.POST.get("selecProvincia", False)
                    )
                    unEstudiante.provincia = provincia
                if request.POST.get("selecCiudad", False) != "0":
                    ciudad = Ciudad.objects.get(
                        pk=request.POST.get("selecCiudad", False)
                    )
                    unEstudiante.ciudad = ciudad

                if request.POST.get("inputTelefono", False) != "":
                    unEstudiante.celular = request.POST.get("inputTelefono", False)
                if request.POST.get("inputDireccion", False) != "":
                    unEstudiante.direccion = request.POST.get("inputDireccion", False)
                # fin datos opcionales

                unEstudiante.foto_perfil = "default/fondo_fotos.jpg"

                unEstudiante.save()

                return JsonResponse({"resultado": 1, "estudiante_id": unEstudiante.id})
        except Exception as ex:
            print(ex)
            return JsonResponse({"resultado": ex})
    else:
        mensaje = "Este método sólo soporta una petición POST"
        print(mensaje)
        return JsonResponse({"resultado": mensaje})


# REGISTRAR FOTO DE PERFIL
@requires_csrf_token
def vwRegistrarFotoPerfilEstudiante(request):
    if request.method == "POST":
        try:
            with transaction.atomic():
                unEstudiante = Estudiante.objects.get(
                    pk=int(request.POST["estudiante_id"])
                )
                unEstudiante.foto_perfil = request.FILES["inputFotoPerfilEstudiante"]
                path_root, ext = os.path.splitext(unEstudiante.foto_perfil.name)
                unEstudiante.foto_perfil.name = (
                    "foto_perfil_" + str(unEstudiante.cedula) + ext
                )

                unEstudiante.save()

            return JsonResponse(
                {"resultado": 1, "foto_perfil_estudiante": unEstudiante.id}
            )
        except Exception as ex:
            print(ex)
            return JsonResponse({"resultado": ex})
    else:
        mensaje = "Este método sólo soporta una petición POST"
        print(mensaje)
        return JsonResponse({"resultado": mensaje})


# REGISTRAR INFORMACIÓN ACADÉMICA
@requires_csrf_token
def vwRegistrarInformacionAcademica(request):
    if request.method == "POST":
        try:
            with transaction.atomic():
                unInformacionAcademica = InformacionAcademica()
                if request.POST.get("inputFechaIngreso", False) != "":
                    unInformacionAcademica.fecha_ingreso = request.POST.get(
                        "inputFechaIngreso", None
                    )
                unInformacionAcademica.numero_carne = request.POST.get(
                    "inputNumeroCarne", ""
                )
                unInformacionAcademica.modalidad_estudios = (
                    ModalidadEstudio.objects.get(
                        pk=request.POST.get("selecModalidaEstudios", None)
                    )
                )
                unInformacionAcademica.jornada = Jornada.objects.get(
                    pk=request.POST.get("selecJornada", None)
                )
                unInformacionAcademica.numero_matricula = NumeroMatricula.objects.get(
                    pk=request.POST.get("selecMatricula", None)
                )
                unInformacionAcademica.estado = Estado.objects.get(
                    pk=request.POST.get("selecEstadoGeneral", None)
                )

                unInformacionAcademica.estudiante = Estudiante.objects.get(
                    pk=int(request.POST["estudiante_id"])
                )
                unInformacionAcademica.save()

                return JsonResponse(
                    {"resultado": 1, "info_academica_id": unInformacionAcademica.id}
                )
        except Exception as ex:
            print(ex)
            return JsonResponse({"resultado": ex})
    else:
        mensaje = "Este método sólo soporta una petición POST"
        print(mensaje)
        return JsonResponse({"resultado": mensaje})


# REGISTRAR HISTORIAL DE CURSOS
@requires_csrf_token
def vwRegistrarHistorialCurso(request):
    if request.method == "POST":
        try:
            with transaction.atomic():
                unCurso = Curso()
                unCurso.estudiante = Estudiante.objects.get(
                    pk=int(request.POST["estudiante_id"])
                )
                unCurso.grado = Grado.objects.get(
                    pk=request.POST.get("selecGrado", False)
                )
                unCurso.nivel = Nivel.objects.get(
                    pk=request.POST.get("selecNivel", False)
                )
                unCurso.paralelo = Paralelo.objects.get(
                    pk=request.POST.get("selecParalelo", False)
                )
                unCurso.especialidad = Especialidad.objects.get(
                    pk=request.POST.get("selecEspecialidad", False)
                )
                unCurso.periodo = Periodo.objects.get(
                    pk=request.POST.get("selecPeriodo", False)
                )
                unCurso.estado = Estado.objects.get(
                    pk=request.POST.get("selecEstado", False)
                )

                unCurso.save()

                return JsonResponse({"resultado": 1, "info_curso_id": unCurso.id})
        except Exception as ex:
            print(ex)
            return JsonResponse({"resultado": ex})
    else:
        mensaje = "Este método sólo soporta una petición POST"
        print(mensaje)
        return JsonResponse({"resultado": mensaje})


# REGISTRAR ANEXOS
@requires_csrf_token
def vwRegistrarAnexo(request):
    if request.method == "POST":
        try:
            with transaction.atomic():
                unEstudiante = Estudiante.objects.get(
                    pk=int(request.POST["estudiante_id"])
                )
                unTipoAnexo = TiposAnexo.objects.get(
                    pk=int(request.POST["selecTipoAnexo"])
                )
                unPeriodo = Periodo.objects.get(
                    pk=int(request.POST["selecPeriodoAnexo"])
                )

                unAnexo = Anexos()
                unAnexo.estudiante = unEstudiante
                unAnexo.tipo_anexo = unTipoAnexo
                unAnexo.periodo = unPeriodo
                unAnexo.archivo = request.FILES["inputAnexo"]

                path_root, ext = os.path.splitext(unAnexo.archivo.name)
                time = datetime.now()
                nombre_archivo = (
                    unTipoAnexo.nombre.lower().replace(" ", "_")
                    + "_"
                    + str(unEstudiante.cedula)
                    + "_"
                    + str(unEstudiante.apellidos)
                    + "_"
                    + time.strftime("%Y-%m-%d")
                    + ext
                )
                unAnexo.archivo.name = nombre_archivo

                unAnexo.save()

                return JsonResponse(
                    {
                        "resultado": 1,
                        "info_anexo_id": unAnexo.id,
                        "info_anexo_name": nombre_archivo,
                        "info_anexo_url": unAnexo.archivo.url,
                    }
                )
        except Exception as ex:
            print(ex)
            return JsonResponse({"resultado": ex})
    else:
        mensaje = "Este método sólo soporta una petición POST"
        print(mensaje)
        return JsonResponse({"resultado": mensaje})


# REGISTRAR REPRESENTANTE
@requires_csrf_token
def vwRegistrarRepresentante(request):
    if request.method == "POST":
        try:
            with transaction.atomic():
                unRepresentante = Representante()
                unRepresentante.estudiante = Estudiante.objects.get(
                    pk=int(request.POST["estudiante_id"])
                )
                unRepresentante.cedula = request.POST["inputCedulaRep"]  # requerido
                unRepresentante.nombres = request.POST["inputNombresRep"]  # requerido
                unRepresentante.apellidos = request.POST[
                    "inputApellidosRep"
                ]  # requerido
                unRepresentante.celular = request.POST.get("inputTelefonoRep", False)

                if request.POST["selecPaisOrigenRep"] != "":
                    unRepresentante.pais = Pais.objects.get(
                        pk=int(request.POST["selecPaisOrigenRep"])
                    )

                if request.POST.get("selecProvinciaRep", False) != "0":
                    unRepresentante.provincia = Provincia.objects.get(
                        pk=int(request.POST["selecProvinciaRep"])
                    )

                if request.POST["selecCiudadRep"] != "":
                    unRepresentante.ciudad = Ciudad.objects.get(
                        pk=int(request.POST["selecCiudadRep"])
                    )

                unRepresentante.direccion = request.POST.get("inputDireccionRep", False)

                unRepresentante.save()

                return JsonResponse(
                    {"resultado": 1, "info_curso_id": unRepresentante.id}
                )
        except Exception as ex:
            print(ex)
            return JsonResponse({"resultado": ex})
    else:
        mensaje = "Este método sólo soporta una petición POST"
        print(mensaje)
        return JsonResponse({"resultado": mensaje})


# EDITAR INFORMACIÓN GENERAL
@requires_csrf_token
def vwEditarInformacionGeneral(request):
    if request.method == "POST":
        try:
            with transaction.atomic():
                estudiante = Estudiante.objects.get(
                    pk=int(request.POST["estudiante_id"])
                )
                estudiante.cedula = request.POST["inputCedula"]
                estudiante.apellidos = request.POST["inputApellidos"]
                estudiante.nombres = request.POST["inputNombres"]

                estudiante.pais = Pais.objects.get(
                    pk=int(request.POST["selecPaisOrigen"])
                )

                if request.POST["inputNacimiento"] == "":
                    estudiante.fecha_nacimiento = None
                else:
                    estudiante.fecha_nacimiento = request.POST.get(
                        "inputNacimiento", False
                    )
                estudiante.correo = request.POST["inputCorreo"]
                estudiante.genero = Genero.objects.get(
                    pk=int(request.POST["selecGenero"])
                )
                estudiante.estado_civil = EstadoCivil.objects.get(
                    pk=int(request.POST["selecEstadoCivil"])
                )
                estudiante.discapacidad = Discapacidad.objects.get(
                    pk=int(request.POST["selecDiscapacidad"])
                )
                estudiante.etnia = Etnia.objects.get(pk=int(request.POST["selecEtnia"]))
                estudiante.cedula = request.POST["inputTelefono"]

                estudiante.provincia = Provincia.objects.get(
                    pk=int(request.POST["selecProvincia"])
                )
                estudiante.ciudad = Ciudad.objects.get(
                    pk=int(request.POST["selecCiudad"])
                )

                if request.POST["inputDireccion"] != "":
                    estudiante.direccion = request.POST.get("inputDireccion", False)

                estudiante.save()
                print("Informacion general guardada con exito")
                return JsonResponse({"resultado": 1})
        except Exception as ex:
            print(ex)
            return JsonResponse({"resultado": 0})
    else:
        mensaje = "Este método sólo soporta una petición POST"
        print(mensaje)
        return JsonResponse({"resultado": mensaje})


# EDITAR FOTO DE PERFIL
@requires_csrf_token
def vwEditarFotoEstudiante(request):
    if request.method == "POST":
        try:
            with transaction.atomic():
                unEstudiante = Estudiante.objects.get(
                    pk=int(request.POST["estudiante_id"])
                )
                print(unEstudiante.foto_perfil.name)
                print(unEstudiante.foto_perfil.url)
                print(unEstudiante.foto_perfil.path)
                unEstudiante.foto_perfil.delete()

                unEstudiante.foto_perfil = request.FILES["inputFotoPerfilEstudiante"]
                path_root, ext = os.path.splitext(unEstudiante.foto_perfil.name)
                unEstudiante.foto_perfil.name = (
                    "foto_perfil_" + str(unEstudiante.cedula) + ext
                )
                unEstudiante.save()

                return JsonResponse({"resultado": 1})
        except Exception as ex:
            print(ex)
            return JsonResponse({"resultado": 0})
    else:
        mensaje = "Este método sólo soporta una petición POST"
        print(mensaje)
        return JsonResponse({"resultado": mensaje})


# EDITAR INFORMACIÓN ACADÉMICA
@requires_csrf_token
def vwEditarInformacionAcademica(request):
    if request.method == "POST":
        try:
            with transaction.atomic():
                existeEstudiante = InformacionAcademica.objects.filter(
                    estudiante_id=int(request.POST["estudiante_id"])
                ).exists()

                if existeEstudiante == False:
                    unInformacionAcademica = InformacionAcademica()
                    unInformacionAcademica.estudiante = Estudiante.objects.get(
                        pk=int(request.POST["estudiante_id"])
                    )
                else:
                    unInformacionAcademica = InformacionAcademica.objects.get(
                        estudiante_id=int(request.POST["estudiante_id"])
                    )

                if request.POST.get("inputFechaIngreso", False) != "":
                    unInformacionAcademica.fecha_ingreso = request.POST.get(
                        "inputFechaIngreso", None
                    )
                unInformacionAcademica.numero_carne = request.POST.get(
                    "inputNumeroCarne", ""
                )
                unInformacionAcademica.modalidad_estudios = (
                    ModalidadEstudio.objects.get(
                        pk=request.POST.get("selecModalidaEstudios", None)
                    )
                )
                unInformacionAcademica.jornada = Jornada.objects.get(
                    pk=request.POST.get("selecJornada", None)
                )
                unInformacionAcademica.numero_matricula = NumeroMatricula.objects.get(
                    pk=request.POST.get("selecMatricula", None)
                )
                unInformacionAcademica.estado = Estado.objects.get(
                    pk=request.POST.get("selecEstadoGeneral", None)
                )
                unInformacionAcademica.save()

                return JsonResponse({"resultado": 1})
        except Exception as ex:
            print(ex)
            return JsonResponse({"resultado": 0})
    else:
        mensaje = (
            "Este método sólo soporta una petición POST vwEditarInformacionAcademica"
        )
        print(mensaje)
        return JsonResponse({"resultado": mensaje})


# EDITAR HISTORIAL DE CURSOS
@requires_csrf_token
def vwEditarHistorialCurso(request):
    if request.method == "POST":
        try:
            with transaction.atomic():
                unCurso = Curso.objects.get(pk=int(request.POST["curso_id"]))
                unCurso.grado = Grado.objects.get(
                    pk=request.POST.get("selecGrado", None)
                )
                unCurso.nivel = Nivel.objects.get(
                    pk=request.POST.get("selecNivel", None)
                )
                unCurso.paralelo = Paralelo.objects.get(
                    pk=request.POST.get("selecParalelo", None)
                )
                unCurso.especialidad = Especialidad.objects.get(
                    pk=request.POST.get("selecEspecialidad", None)
                )
                unCurso.periodo = Periodo.objects.get(
                    pk=request.POST.get("selecPeriodo", None)
                )
                unCurso.estado = Estado.objects.get(
                    pk=request.POST.get("selecEstado", None)
                )

                unCurso.save()

                return JsonResponse(
                    {
                        "resultado": 1,
                        "curso_id": unCurso.id,
                        "grado": unCurso.grado.nombre,
                        "nivel": unCurso.nivel.nombre,
                        "paralelo": unCurso.paralelo.nombre,
                        "especialidad": unCurso.especialidad.nombre,
                        "periodo": unCurso.periodo.nombre,
                        "estado": unCurso.estado.nombre,
                        "estado_id": unCurso.estado.id,
                    },
                    safe=False,
                )
        except Exception as ex:
            print(ex)
            return JsonResponse({"resultado": 0})
    else:
        mensaje = "Este método sólo soporta una petición POST vwEditarInformacionCurso"
        print(mensaje)
        return JsonResponse({"resultado": mensaje})


# EDITAR ANEXOS
@requires_csrf_token
def vwEditarAnexos(request):
    if request.method == "POST":
        try:
            with transaction.atomic():
                return JsonResponse({"resultado": 1})
        except Exception as ex:
            print(ex)
            return JsonResponse({"resultado": 0})
    else:
        mensaje = "Este método sólo soporta una petición POST"
        print(mensaje)
        return JsonResponse({"resultado": mensaje})


# EDITAR REPRESENTANTE
@requires_csrf_token
def vwEditarRepresentante(request):
    if request.method == "POST":
        try:
            existeRepresentante = Representante.objects.filter(
                estudiante_id=int(request.POST["estudiante_id"])
            ).exists()

            if existeRepresentante == False:
                unRepresentante = Representante()
                unRepresentante.estudiante = Estudiante.objects.get(
                    pk=int(request.POST["estudiante_id"])
                )
            else:
                unRepresentante = Representante.objects.get(
                    estudiante_id=int(request.POST["estudiante_id"])
                )

            unRepresentante.cedula = request.POST["inputCedulaRep"]  # requerido
            unRepresentante.nombres = request.POST["inputNombresRep"]  # requerido
            unRepresentante.apellidos = request.POST["inputApellidosRep"]  # requerido
            unRepresentante.celular = request.POST.get("inputTelefonoRep", None)

            if request.POST["selecPaisOrigenRep"] != "":
                unRepresentante.pais = Pais.objects.get(
                    pk=int(request.POST["selecPaisOrigenRep"])
                )

            if request.POST["selecProvinciaRep"] != "":
                unRepresentante.provincia = Provincia.objects.get(
                    pk=int(request.POST["selecProvinciaRep"])
                )

            if request.POST["selecCiudadRep"] != "":
                unRepresentante.ciudad = Ciudad.objects.get(
                    pk=int(request.POST["selecCiudadRep"])
                )

            unRepresentante.direccion = request.POST.get("inputDireccionRep", None)
            unRepresentante.save()

            with transaction.atomic():
                return JsonResponse({"resultado": 1})
        except Exception as ex:
            print(ex)
            return JsonResponse({"resultado": 0})
    else:
        mensaje = "Este método sólo soporta una petición POST"
        print(mensaje)
        return JsonResponse({"resultado": mensaje})


# ELIMINAR ESTUDIANTE
@requires_csrf_token
def vwEliminarEstudiante(request):
    if request.method == "POST":
        try:
            with transaction.atomic():
                # Borrado seguro
                # se recomienda cambiar el estado *eliminado* del estudiante a True
                unEstudiante = Estudiante.objects.get(
                    pk=int(request.POST["estudiante_id"])
                )
                unEstudiante.eliminado = True
                unEstudiante.save()
                return JsonResponse({"resultado": 1})
        except Exception as ex:
            print(ex)
            return JsonResponse({"resultado": ex})
    else:
        mensaje = "Este método sólo soporta una petición POST"
        print(mensaje)
        return JsonResponse({"resultado": mensaje})


# ELIMINAR CURSO
@requires_csrf_token
def vwEliminarCurso(request):
    if request.method == "POST":
        try:
            with transaction.atomic():
                unCurso = Curso.objects.get(pk=int(request.POST["curso_id"]))
                unCurso.delete()

                return JsonResponse({"resultado": 1})
        except Exception as ex:
            print(ex)
            return JsonResponse({"resultado": ex})
    else:
        mensaje = "Este método sólo soporta una petición POST"
        print(mensaje)
        return JsonResponse({"resultado": mensaje})


# ELIMINAR ANEXO
@requires_csrf_token
def vwEliminarAnexo(request):
    if request.method == "POST":
        try:
            with transaction.atomic():
                unAnexo = Anexos.objects.get(pk=int(request.POST["anexo_id"]))
                unAnexo.archivo.delete()
                unAnexo.delete()

                return JsonResponse({"resultado": 1})
        except Exception as ex:
            print(ex)
            return JsonResponse({"resultado": ex})
    else:
        mensaje = "Este método sólo soporta una petición POST"
        print(mensaje)
        return JsonResponse({"resultado": mensaje})


# Generar reporte
def generate_pdf_report_estudent(request):
    if request.method == "GET":
        students = Estudiante.objects.filter(eliminado=False)[:50]
        # crear el response object con pdf contentype
        response = HttpResponse(content_type="application/pdf")
        response[
            "Content-Disposition"
        ] = 'attachment; filename="reporte_estudiantes.pdf"'

        # crear el pdf
        pdf = canvas.Canvas(response)
        # set fuente y tamaño
        pdf.setFont("Helvetica", 12)
        pdf.drawString(200, 800, "Reporte de Estudiantes")
        y = 700  # posicion inicial
        for student in students:
            pdf.drawString(
                50, y, "Nombre: " + str(student.nombre) + " " + str(student.apellidos)
            )
            pdf.drawString(50, y - 20, "Cedula: " + str(student.cedula))
            pdf.drawString(50, y - 40, "Telefono: " + str(student.celular))
            pdf.drawString(50, y - 60, "Direccion: " + str(student.direccion))
            pdf.drawString(50, y - 80, "Genero: " + str(student.genero))
            pdf.drawString(50, y - 100, "Estado: " + str(student.estado))
            pdf.drawString(50, y - 120, "Discapacidad: " + str(student.discapacidad))
            pdf.drawString(50, y - 140, "Etnia: " + str(student.etnia))
            pdf.drawString(50, y - 160, "Provincia: " + str(student.provincia))
            pdf.drawString(50, y - 180, "Ciudad: " + str(student.ciudad))
            pdf.drawString(
                50, y - 200, "Fecha Nacimiento: " + str(student.fecha_nacimiento)
            )
            pdf.drawString(50, y - 220, "Nacionalidad: " + str(student.nacionalidad))
            pdf.drawString(50, y - 240, "Estado Civil: " + str(student.estado_civil))
            pdf.drawString(50, y - 260, "Grado: " + str(student.grado))
            pdf.drawString(50, y - 280, "Nivel: " + str(student.nivel))
            pdf.drawString(50, y - 300, "Paralelo: " + str(student.paralelo))
            pdf.drawString(50, y - 320, "Especialidad: " + str(student.especialidad))
            pdf.drawString(50, y - 340, "Periodo: " + str(student.periodo))
            y -= 20
        pdf.showPage()
        pdf.save()
        return response
    else:
        mensaje = "Este método sólo soporta una petición GET"
        print(mensaje)
        return JsonResponse({"resultado": mensaje})

def popultaion_chart(request):
    labesl = []
    data = []

    from django.db.models import Count

    queryset = Curso.objects.values('periodo__nombre', 'estudiante__genero__nombre').annotate(
        student_count=Count('estudiante__genero__nombre')).order_by('-periodo__nombre')

    for entry in queryset:
        labesl.append(entry['periodo__nombre'])
        data.append(entry['estudiante__genero__nombre'])

    return JsonResponse(data={
        'labels':labesl,
        'data':data,
    })