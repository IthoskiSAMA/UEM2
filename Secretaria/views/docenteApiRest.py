from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Sum
from Modelos.models import *
from django.views.decorators.csrf import requires_csrf_token
from django.core.exceptions import ObjectDoesNotExist
import os
from datetime import datetime

#verificar si el usuario esta logueado
def verificarLogin(request):
    if request.session.get("usuario") is None:
        return False
    else:
        return True

#verificar si la cedula ya esta registrada mediante metodo post en el formulario de agregar docente
def verificarCedulaDocente(request):
    if request.method == "POST":
        try:
            with transaction.atomic():
                existeDocente = Docente.objects.filter(
                    cedula=request.POST["cedula"]
                ).exists()
                if existeDocente == False:
                    return JsonResponse({"resultado": 1})
                else:
                    return JsonResponse({"resultado": 0})
        except Exception as ex:
            return JsonResponse({"resultado": -1})
    else:
        return JsonResponse({"resultado": "Este método sólo soporta una petición POST"})

# obtener lista de docentes
@requires_csrf_token
def getJsonObtenerDocentes(request):
    if request.method == "GET":
        response = list(Docente.objects.values())
        if response == []:
            return JsonResponse({"resultado": 0})

        return JsonResponse({"resultado": 1, "listaDocentes": response})
    else:
        return JsonResponse({"resultado": "Este método sólo soporta una petición GET"})

# BUSCAR DOCENTE
@requires_csrf_token
def getJsonBuscarDocente(request):
    if request.method == 'POST':
        datos = request.POST['inputDatos']
        response = None

        if request.POST['selecBuscar'] == 'cedula':
            response = list(Docente.objects.filter(cedula__icontains = datos, eliminado = False)[:50].values())
        
        elif request.POST['selecBuscar'] == 'apellidos':
            response = list(Docente.objects.filter(apellidos__icontains = datos, eliminado = False)[:50].values())

        elif request.POST['selecBuscar'] == 'nombres':
            response = list(Docente.objects.filter(nombres__icontains = datos, eliminado = False)[:50].values())

        else:
            return JsonResponse({'resultado': 0})

        if (response == []):
            return JsonResponse({'resultado': 0})
        
        return JsonResponse({'resultado': 1, "listaDocentes": response})
    else:
        mensaje = "Este método sólo soporta una petición POST"
        print(mensaje)
        # 1 -> success
        # 0 -> fail
        # -1 -> error
        return JsonResponse({'resultado': mensaje})

# registrar docente
def vwRegistrarDocente(request):
        if request.method == "POST":
            try:
                with transaction.atomic():
                    cedula = request.POST.get("inputCedula")
                    nombre = request.POST.get("inputNombres")
                    apellido = request.POST.get("inputApellidos")
                    foto_perfil = request.FILES.get("inputFotoPerfil")
                    nivel_educacion = request.POST.get("inputNEducacion")
                    titulo_3_nivl = request.POST.get("inputTNivel")
                    titulo_4_nivl = request.POST.get("inputCNivel")
                    especialidad = request.POST.get("inputEspecialidad")
                    if (request.POST.get('selecEtnia', False) != '0'):
                        etnia = Etnia.objects.get(pk = request.POST.get('selecEtnia', False))
                    relacion_laboral = request.POST.get("inputRLaboral")
                    funcion_cargo = request.POST.get("inputFCargo")
                    funcion_2 = request.POST.get("inputFuncion2")
                    categoria = request.POST.get("inputCategoria")
                    fecha_nacimiento = request.POST.get("inputFechaNacimiento")
                    edad = request.POST.get("inputEdad")
                    fecha_ingreso_magisterio = request.POST.get("inputFechaIngresoM")
                    anos_magisterio = request.POST.get("inputAnosMagisterio")
                    fecha_ingreso_IE = request.POST.get("inputFechaIngresoIE")
                    anos_servicio_IE = request.POST.get("inputAnosIE")
                    lugar_residencia = request.POST.get("inputLugarR")
                    celular = request.POST.get("inputCelular")
                    correo = request.POST.get("inputCorreo")
                    correo_institucional = request.POST.get("inputCorreoInsti")
                    # Guardar Docente
                    docente = Docente(
                        cedula=cedula,
                        nombres=nombre,
                        apellidos=apellido,
                        foto_perfil=foto_perfil,
                        nivel_educacion=nivel_educacion,
                        titulo_tercer_nivel=titulo_3_nivl,
                        titulo_cuarto_nivel=titulo_4_nivl,
                        especialidad=especialidad,
                        grupo_etnico=etnia,
                        relacion_laboral=relacion_laboral,
                        funcion_cargo=funcion_cargo,
                        funcion_2=funcion_2,
                        categoria=categoria,
                        fecha_nacimiento=fecha_nacimiento,
                        edad=edad,
                        fecha_ingreso_magisterio=fecha_ingreso_magisterio,
                        anos_servicio_magisterio=anos_magisterio,
                        fecha_ingreso_ie=fecha_ingreso_IE,
                        anos_servicio_ie=anos_servicio_IE,
                        lugar_recidencia=lugar_residencia,
                        celular=celular,
                        correo=correo,
                        correo_institucional=correo_institucional,
                    )
                    docente.save()
                    #print(docente)
                    return JsonResponse({"resultado": 1})
            except Exception as e:
                print(e)
                return JsonResponse({"resultado": 0})
        else:
            return render(request, "docentes/docnt_agregar.html")

# REGISTRAR FOTO DE PERFIL
@requires_csrf_token
def vwRegistrarFotoPerfilDocente(request):
    if request.method == "POST":
        try:
            with transaction.atomic():
                unDocente = Docente.objects.get(
                    pk=int(request.POST["docente_id"])
                )
                unDocente.foto_perfil = request.FILES["inputFotoPerfilDocente"]
                path_root, ext = os.path.splitext(unDocente.foto_perfil.name)
                unDocente.foto_perfil.name = (
                    "foto_perfil_" + str(unDocente.cedula) + ext
                )

                unDocente.save()

            return JsonResponse(
                {"resultado": 1, "foto_perfil_docente": unDocente.id}
            )
        except Exception as ex:
            print(ex)
            return JsonResponse({"resultado": ex})
    else:
        mensaje = "Este método sólo soporta una petición POST"
        print(mensaje)
        return JsonResponse({"resultado": mensaje})

# ELIMINAR ESTUDIANTE
@requires_csrf_token
def vwEliminarDocente(request):
    if request.method == "POST":
        try:
            with transaction.atomic():
                # Borrado seguro
                # se recomienda cambiar el estado *eliminado* del estudiante a True
                unDocente = Docente.objects.get(
                    pk=int(request.POST["docente_id"])
                )
                unDocente.eliminado = True
                unDocente.save()
                return JsonResponse({"resultado": 1})
        except Exception as ex:
            print(ex)
            return JsonResponse({"resultado": ex})
    else:
        mensaje = "Este método sólo soporta una petición POST"
        print(mensaje)
        return JsonResponse({"resultado": mensaje})
    
# EDITAR DOCENTE 
@requires_csrf_token
def vwEditarDocente(request):
    if request.method == "POST":
        try:
            with transaction.atomic():
                docente = Docente.objects.get(
                    pk=int(request.POST["docente_id"])
                )
                docente.cedula = request.POST.get("inputCedula")
                docente.nombres = request.POST.get("inputNombres")
                docente.apellidos = request.POST.get("inputApellidos")
                docente.nivel_educacion = request.POST.get("inputNEducacion")
                docente.titulo_tercer_nivel = request.POST.get("inputTNivel")
                docente.titulo_cuarto_nivel = request.POST.get("inputCNivel")
                docente.especialidad = request.POST.get("inputEspecialidad")
                if (request.POST.get('selecEtnia', False) != '0'):
                    docente.grupo_etnico = Etnia.objects.get(pk = request.POST.get('selecEtnia', False))
                docente.relacion_laboral = request.POST.get("inputRLaboral")
                docente.funcion_cargo = request.POST.get("inputFCargo")
                docente.funcion_2 = request.POST.get("inputFuncion2")
                docente.categoria = request.POST.get("inputCategoria")
                docente.fecha_nacimiento = request.POST.get("inputFechaNacimiento")
                docente.edad = request.POST.get("inputEdad")
                docente.fecha_ingreso_magisterio = request.POST.get("inputFechaIngresoM")
                docente.anos_servicio_magisterio = request.POST.get("inputAnosMagisterio")
                docente.fecha_ingreso_ie = request.POST.get("inputFechaIngresoIE")
                docente.anos_servicio_ie = request.POST.get("inputAnosIE")
                docente.lugar_recidencia = request.POST.get("inputLugarR")
                docente.celular = request.POST.get("inputCelular")
                docente.correo = request.POST.get("inputCorreo")
                docente.correo_institucional = request.POST.get("inputCorreoInsti")
                docente.save()

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
def vwEditarFotoDocente(request):
    if request.method == "POST":
        try:
            with transaction.atomic():
                unDocente = Docente.objects.get(
                    pk=int(request.POST["docente_id"])
                )
                print(unDocente.foto_perfil.name)
                print(unDocente.foto_perfil.url)
                print(unDocente.foto_perfil.path)
                unDocente.foto_perfil.delete()

                unDocente.foto_perfil = request.FILES["inputFotoPerfilDocente"]
                path_root, ext = os.path.splitext(unDocente.foto_perfil.name)
                unDocente.foto_perfil.name = (
                    "foto_perfil_" + str(unDocente.cedula) + ext
                )
                unDocente.save()

                return JsonResponse({"resultado": 1})
        except Exception as ex:
            print(ex)
            return JsonResponse({"resultado": 0})
    else:
        mensaje = "Este método sólo soporta una petición POST"
        print(mensaje)
        return JsonResponse({"resultado": mensaje})
