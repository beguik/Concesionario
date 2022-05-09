from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from .models import *
from django.db.models import Q

# Create your views here.
class InicioView(ListView):
    template_name = 'inicio.html'
    #success_url = '/prueba'
    model = Coche
    fields = ('__all__')
    context_object_name = 'formu'

    def get_queryset(self):
        try:
            buscar_clave = self.request.GET.get("busqueda", '')
            if buscar_clave == 'Marca, Modelo, Matricula':
                palabra_clave = self.request.GET.get("kword", '')
                return Coche.objects.listar_coches_kword(palabra_clave)
            elif buscar_clave == 'Fecha inferior a Año-Mes-Dia':
                fecha_clave = self.request.GET.get("kword", '')
                return Coche.objects.listar_coches_ltfecha(fecha_clave)
            else:
                return Coche.objects.all()
        except:
            return Coche.objects.all()

    def listar_coches_kword(self, kword):
        lista = self.filter(
            Q(marcanombreicontains=kword) | Q(matriculaicontains=kword) | Q(modelonombreicontains=kword),
        )
        return lista

    def listar_coches_ltfecha(self, kword):
        lista = self.filter(
            fecha_creacionlte = kword
        )
        return lista