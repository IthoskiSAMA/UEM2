from django.db import transaction
from django.db import transaction
from Modelos.forms import DocenteForm
from Modelos.models import *
from django.views.decorators.csrf import requires_csrf_token
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
import os
from datetime import datetime


# VERIFICAR SI LA CÉDULA YA ESTÁ REGISTRADA
@requires_csrf_token
def getJsonVerificarExisteDocente(request):
    if request.method == "POST":
        try:
            with transaction.atomic():
                existeDocente = Docente.objects.filter(cedula = request.POST['cedula']).exists()
                if (existeDocente == False):
                    return JsonResponse({'resultado': 1})
                else:
                    return JsonResponse({'resultado': 0})
        except Exception as ex:
            return JsonResponse({'resultado': -1})
    else:
        return JsonResponse({'resultado': "Este método sólo soporta una petición POST"})

# OBTENER CIUDADES POR PROVINCIA
def getJsonCiudadesXProvincia(request):
    if request.method == 'GET':
        try:
            ciudades = list(Ciudad.objects.values())
            return JsonResponse(ciudades, safe=False)
        except Exception as ex:
            print(ex)
            return JsonResponse({'resultado': ex})
    else:
        mensaje = "Este método sólo soporta petición GET"
        print(mensaje)
        return JsonResponse({'resultado': mensaje})

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

# OBTENER LISTA DE DOCENTES
def getJsonObtenerDocentes(request):
    if request.method == 'GET':
        response = list(Docente.objects.values())
        if (response == []):
            return JsonResponse({'resultado': 0})
        
        return JsonResponse({'resultado': 1, "listaDocentes": response})
    else:
        return JsonResponse({'resultado': "Este método sólo soporta una petición GET"})

# REGISTRAR INFORMACIÓN GENERAL
@requires_csrf_token
def vwRegistrarInformacionGeneral(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # datos requeridos
                unDocente = Docente()
                unDocente.nombres = request.POST['inputNombres']
                unDocente.apellidos = request.POST['inputApellidos']
                unDocente.cedula = request.POST['inputCedula']
                # fin datos requeridos

                # datos opcionales
                unDocente.nivel_educacion = request.POST['inputEducacion']
                unDocente.titulo_tercer_nivel = request.POST['inputTNivel']
                unDocente.titulo_cuarto_nivel = request.POST['inputCNivel']
                unDocente.especialidad = request.POST['inputEspecialidad']
                if (request.POST.get('selecEtnia', False) != '0'):
                    etnia = Etnia.objects.get(pk = request.POST.get('selecEtnia', False))
                    unDocente.grupo_etnico = etnia
                unDocente.relacion_laboral = request.POST['inputRLaboral']
                unDocente.funcion_cargo = request.POST['inputFCargo']
                unDocente.funcion_2 = request.POST['inputFuncion2']
                unDocente.categoria = request.POST['inputCategoria']
                unDocente.fecha_nacimiento = request.POST['inputFechaNacimiento']
                unDocente.edad = request.POST['inputEdad']
                unDocente.fecha_ingreso_magisterio = request.POST['inputFechaIngresoM']
                unDocente.anos_servicio_magisterio = request.POST['inputAnosMagisterio']
                unDocente.fecha_ingreso_ie = request.POST['inputFechaIngresoIE']
                unDocente.anos_servicio_ie = request.POST['inputAnosIE']
                unDocente.lugar_recidencia = request.POST['inputLugarR']
                unDocente.celular = request.POST['inputCelular']
                unDocente.correo = request.POST['inputCorreo']
                unDocente.correo_institucional = request.POST['inputCorreoInsti']
                # fin datos opcionales

                unDocente.foto_perfil = "default/fondo_fotos.jpg"
                unDocente.save()
                #unDocente.save()

                return JsonResponse({"resultado": 1, "docente_id": unDocente.id})
        except Exception as ex:
            print(ex)
            return JsonResponse({"resultado": ex})
    else:
        mensaje = "Este método sólo soporta una petición POST"
        print(mensaje)
        return JsonResponse({"resultado": mensaje})

@requires_csrf_token
def vwRegistrarInformacionGeneralDocente(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                docente = Docente.objects.get(pk=int(request.POST['docente_id']))
                form = DocenteForm(request.POST, instance=docente)  # Usar el formulario con la instancia existente

                if form.is_valid():
                    form.save()
                    print("Información general actualizada exitosamente")
                    return JsonResponse({'resultado': 1})
                else:
                    # Si hay errores en el formulario, devuelve los errores en la respuesta JSON
                    errors = form.errors.as_json()
                    return JsonResponse({'resultado': 0, 'errors': errors})
        except Exception as ex:
            print(ex)
            return JsonResponse({'resultado': 0})
    else:
        mensaje = "Este método solo soporta una petición POST"
        print(mensaje)
        return JsonResponse({'resultado': mensaje})


# EDITAR INFORMACIÓN GENERAL
@requires_csrf_token
def vwEditarInformacionGeneral(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                docente = Docente.objects.get(pk = int(request.POST['docente_id']))
                docente.cedula = request.POST['inputCedula']
                docente.apellidos = request.POST['inputApellidos']
                docente.nombres = request.POST['inputNombres']
                
                if (request.POST['inputEducacion'] != ""):
                    docente.nivel_educacion = request.POST.get('inputEducacion', False)
                if (request.POST['inputTNivel'] != ""):
                    docente.titulo_tercer_nivel = request.POST.get('inputTNivel', False)
                if (request.POST['inputCNivel'] != ""):
                    docente.titulo_cuarto_nivel = request.POST.get('inputCNivel', False)
                if (request.POST['inputEspecialidad'] != ""):
                    docente.especialidad = request.POST.get('inputEspecialidad', False)
                docente.grupo_etnico = Etnia.objects.get(pk = int(request.POST['selecEtnia']))
                if (request.POST['inputRLaboral'] != ""):
                    docente.relacion_laboral = request.POST.get('inputRLaboral', False)
                if (request.POST['inputFCargo'] != ""):
                    docente.funcion_cargo = request.POST.get('inputFCargo', False)
                if (request.POST['inputFuncion2'] != ""):
                    docente.funcion_2 = request.POST.get('inputFuncion2', False)
                if (request.POST['inputCategoria'] != ""):
                    docente.categoria = request.POST.get('inputCategoria', False)
                if (request.POST['inputNacimiento'] == ""):
                    docente.fecha_nacimiento = None
                else:
                    docente.fecha_nacimiento = request.POST.get('inputNacimiento', False)
                if (request.POST['inputEdad'] != ""):
                    docente.edad = request.POST.get('inputEdad', False)
                if (request.POST['inputFechaIngresoM'] == ""):
                    docente.fecha_ingreso_magisterio = None
                else:
                    docente.fecha_ingreso_magisterio = request.POST.get('inputFechaIngresoM', False)
                if (request.POST['inputAnosMagisterio'] != ""):
                    docente.anos_servicio_magisterio = request.POST.get('inputAnosMagisterio', False)
                if (request.POST['inputFechaIngresoIE'] == ""):
                    docente.fecha_ingreso_ie = None
                else:
                    docente.fecha_ingreso_ie = request.POST.get('inputFechaIngresoIE', False)
                if (request.POST['inputAnosIE'] != ""):
                    docente.anos_servicio_ie = request.POST.get('inputAnosIE', False)
                if (request.POST['inputLugarR'] != ""):
                    docente.lugar_recidencia = request.POST.get('inputLugarR', False)
                if (request.POST['inputCelular'] != ""):
                    docente.celular = request.POST.get('inputCelular', False)
                if (request.POST['inputCorreo'] != ""):
                    docente.correo = request.POST.get('inputCorreo', False)
                if (request.POST['inputCorreoInsti'] != ""):
                    docente.correo_institucional = request.POST.get('inputCorreoInsti', False)
                docente.save()
                print("Informacion general guardada con exito")
                return JsonResponse({'resultado': 1})
        except Exception as ex:
            print(ex)
            return JsonResponse({'resultado': 0})
    else:
        mensaje = "Este método sólo soporta una petición POST"
        print(mensaje)
        return JsonResponse({'resultado': mensaje})

# REGISTRAR FOTO DE PERFIL
@requires_csrf_token
def vwRegistrarFotoPerfilDocente(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                unDocente = Docente.objects.get(pk = int(request.POST['docente_id']))
                unDocente.foto_perfil = request.FILES['inputFotoPerfilDocente']
                path_root, ext = os.path.splitext(unDocente.foto_perfil.name)
                unDocente.foto_perfil.name = "foto_perfil_" + str(unDocente.cedula) + ext

                unDocente.save()

            return JsonResponse({'resultado': 1, 'foto_perfil_docente': unDocente.id})
        except Exception as ex:
            print(ex)
            return JsonResponse({'resultado': ex})
    else:
        mensaje = "Este método sólo soporta una petición POST"
        print(mensaje)
        return JsonResponse({'resultado': mensaje})

# EDITAR FOTO DE PERFIL
@requires_csrf_token
def vwEditarFotoDocente(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                unDocente = Docente.objects.get(pk = int(request.POST['docente_id']))
                print(unDocente.foto_perfil.name)
                print(unDocente.foto_perfil.url)
                print(unDocente.foto_perfil.path)
                unDocente.foto_perfil.delete()

                unDocente.foto_perfil = request.FILES['inputFotoPerfilDocente']
                path_root, ext = os.path.splitext(unDocente.foto_perfil.name)
                unDocente.foto_perfil.name = "foto_perfil_" + str(unDocente.cedula) + ext
                unDocente.save()

                return JsonResponse({'resultado': 1})
        except Exception as ex:
            print(ex)
            return JsonResponse({'resultado': 0})
    else:
        mensaje = "Este método sólo soporta una petición POST"
        print(mensaje)
        return JsonResponse({'resultado': mensaje})