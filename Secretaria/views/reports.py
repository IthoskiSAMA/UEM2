import io

import base64
from django.db.models import Count
from django.shortcuts import render


from Modelos.models import *
import matplotlib.pyplot as plt


#probar para reportes
# Página del Tablero
def mostrarPeriodo(request):

    anolectivo = Periodo.objects.all()
    list_anos = []
    for ano in anolectivo:
        list_anos.append({
            'id': ano.id,
            'nombre': ano.nombre,
        })
    print("Veamos que sale")
    print(list_anos)

    return render(request, 'reportes/reportes-estudiantes.html', {
        'list_anos': list_anos,
    })

def generar_grafico(anio):
    genero = Genero.objects.all()
    estudiantes = Estudiante.objects.filter(curso__periodo__nombre=anio)
    datos = estudiantes.values('genero__nombre').annotate(cantidad=Count('genero__nombre'))
    labels = []
    counts = []
    for dato in datos:
        labels.append(dato['genero__nombre'])
        counts.append(dato['cantidad'])
    plt.bar(labels, counts)
    plt.xlabel('Genero')
    plt.ylabel('Numero de Estudiantes')
    plt.title('Grafico de Barras . Alumnos por Género ({anio})')
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    return graph
