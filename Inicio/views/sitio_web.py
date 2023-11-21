from django.shortcuts import render
from Modelos.models import *

def pageIndex(request):
    cant_estudiantes = Estudiante.objects.count()
    return render(request,'sitio_web/index.html',{'cant_estudiantes':cant_estudiantes})

def pageSobreNosotros(request):
    return render(request, 'sitio_web/sobre_nosotros.html')

def pageContacto(request):
    return render(request, 'sitio_web/index.html')

def pageBlogs(request):
    return render(request, 'sitio_web/index.html')