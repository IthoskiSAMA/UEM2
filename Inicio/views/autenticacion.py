from django.shortcuts import render, redirect
from django.http import JsonResponse
from Inicio.models import Usuario


def pageLogin(request):
    return render(request, 'autenticacion/login.html')

def pageRecuperarPassword(request):
    return render(request, 'autenticacion/recuperar-password.html')

def getJsonIniciarSesion(request):
    if request.method == 'POST':
        correo = request.POST['inputCorreo']
        password = request.POST['inputPassword']

        usuario = Usuario.objects.filter(correo = correo, password = password).first()
        if usuario:
            request.session['usuarioID'] = usuario.id
            request.session['usuarioNombre'] = usuario.nombre
            request.session['usuarioRol'] = usuario.rol.nombre
            return JsonResponse({'resultado': 1})
        return JsonResponse({'resultado': 0})
        
    else:
        return JsonResponse({'resultado': "Este método sólo soporta una petición POST"})

def getJsonVerificarCorreo(request):
    # Deben comprobar que el correo que quiere recuperar la clave exista en la base de datos
    # Devolver true o falso para indicar que existe o no
    return JsonResponse({'resultado': False})

def getJsonEnviarPasswordXCorreo(request):
    # Enviar la constraseña del usuario al correo registrado
    # Devolver un json de confirmación
    return JsonResponse({'resultado': True}) # True = Mensaje enviado al correo

def cerrarSesion(request):
    if request.session.get('usuarioID'):
        del request.session['usuarioID']
        del request.session['usuarioNombre']
        del request.session['usuarioRol']
        request.session.flush()
    
    return redirect('/')