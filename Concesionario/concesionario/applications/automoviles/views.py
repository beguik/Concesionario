from django.shortcuts import render
from django.views.generic import TemplateView, ListView, View
from .models import *
from django.db.models import FilteredRelation, Q
from datetime import datetime 
from django.db.models import Max
from django.core.paginator import Paginator
import collections
import hashlib


# Create your views here.
class InicioView(ListView):
   
    def get(self,request):
        filtro=Coche.objects.all()
        tipos=TiposCoches.objects.all()
        respuesta=Coche.objects.all() 
        paginator=Paginator(respuesta,4)
        page_number=request.GET.get('page')
        resultado =paginator.get_page(page_number)



        return render(request,"inicio.html",{"filtro":filtro,"resultado":resultado, "tipos":tipos})


    
class Inicio_v2(View):
    model=Coche

    def get(self,request):
        filtro=Coche.objects.all()
        tipos=TiposCoches.objects.all() 
        provincia= Coche.PROVINCE_CHOICES
        respuesta=Coche.objects.all() 
        paginator=Paginator(respuesta,4)
        page_number=request.GET.get('page')
        resultado =paginator.get_page(page_number)

        return render(request,"inicio.html",{"filtro":filtro,"resultado":resultado,"tipos":tipos, "provincia":provincia})
    
    def post(self,request):
        
        precio=Coche.objects.all().aggregate(Max('precio_original'))
        kilometros_max=Coche.objects.all().aggregate(Max('kilometros'))
        datos2=request.POST
        datos=datos2.copy()
        
        for i in datos.keys():
            logs("log_prueba",str(datos[i]))
            if i=="fecha":
                if datos[i]=="default":
                    datos[i]=(f"1885-1-1:{datetime.now().strftime('%Y-%m-%d')}")
                else:
                    datos[i]=(f"1885-1-1:{fecha_a_normal(datos[i])}")
            elif i =="precio":
                if datos[i]=="default":
                    datos[i]=(f"0-{precio['precio_original__max']}")
            elif i =="kilometros":
                if datos[i]=="default":
                    datos[i]=(f'0-{kilometros_max["kilometros__max"]}')
                else:
                    datos[i]=(f'{datos[i]}')
            elif datos[i]=="default":     
                datos[i]=""

        resultado=Coche.objects.filter(
            Q(modelo__nombre__icontains=datos["modeloselect"]) &
            Q(modelo__marca__nombre__icontains=datos["marcaselect"]) &
            Q(fecha_matriculacion__lte=datos["fecha"].split(":")[1]) &
            Q(fecha_matriculacion__gte=datos["fecha"].split(":")[0]) &
            Q(tipo__tipo__icontains=datos["tipo"]) &
            Q(cambio__icontains=datos["cambio"]) &
            Q(kilometros__gte=datos["kilometros"].split("-")[0]) &
            Q(kilometros__lte=datos["kilometros"].split("-")[1]) &
            Q(localizacion__icontains=datos["local"]) &
            Q(precio_original__gte=datos["precio"].split("-")[0]) &
            Q(precio_original__lte=datos["precio"].split("-")[1]),
            )

        paginator=Paginator(resultado,4)
        page_number=request.GET.get('page')
        resultado =paginator.get_page(page_number)

        logs("log_diccionario",str(datos))
        return render(request, "inicio.html",{ "resultado":resultado, "filtro":Coche.objects.all() 
                                         })
def fecha_a_normal(fecha):
    fecha_cv=fecha.split("de")
    contador=1
   
    fecha_cv[0]=str(fecha_cv[0]).replace(" ","")
    fecha_cv[1]=str(fecha_cv[1]).replace(" ","")
    fecha_cv[2]=str(fecha_cv[2]).replace(" ","")
    fecha
    lista_meses=["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
    for i in lista_meses:
        
        if i == str(fecha_cv[1]):
            fecha_cv[1]=str(contador)
           
            return str(str(fecha_cv[2])+"-"+str(fecha_cv[1])+"-"+str(fecha_cv[0]))
        elif fecha_cv[1] in lista_meses:
            contador=contador+1
      
def logs(file="log",mensaje=""):
    escribir = open(file, "a")
    escribir.write(mensaje+"\n")
    escribir.close()