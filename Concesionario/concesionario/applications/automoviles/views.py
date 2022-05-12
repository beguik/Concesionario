from django.shortcuts import render
from django.views.generic import TemplateView, ListView, View
from .models import *
from django.db.models import FilteredRelation, Q
from datetime import datetime 
from django.db.models import Max
from django.core.paginator import Paginator
from .choices import *
import collections
import hashlib



# Create your views here.
    
class Inicio(View):
    model=Coche

    def get(self,request):
        
        marca=Marca.objects.all()
        modelo=Modelo.objects.all()
        filtro=Coche.objects.all()
        tipos=TiposCoches.objects.all() 
        provincia= lista_fuc(PROVINCE_CHOICES)
        cambios= lista_fuc(CAMBIO_CHOICES)
        respuesta=Coche.objects.all() 
        paginator=Paginator(respuesta,4)
        page_number=request.GET.get('page')
        resultado =paginator.get_page(page_number)
        
        
        return render(request,"inicio.html",{"fecha":datetime.now().strftime('%Y-%m-%d'),"filtro":filtro,"resultado":resultado,"tipos":tipos, "provincia":provincia,"marca":marca, "modelo":modelo, "cambios":cambios,})
    
    def post(self,request):
        
        marca=Marca.objects.all()
        modelo=Modelo.objects.all()
        tipos=TiposCoches.objects.all() 
        provincia= lista_fuc(PROVINCE_CHOICES)
        cambios= lista_fuc(CAMBIO_CHOICES)
        precio=Coche.objects.all().aggregate(Max('precio_original'))
        kilometros_max=Coche.objects.all().aggregate(Max('kilometros'))
        datos2=request.POST
        datos=datos2.copy()

        if 'modeloselect' not in datos.keys():
            datos.update({'modeloselect': ''})
        
        for i in datos.keys():
            logs("log_prueba",str(datos[i]))
            if i=="fecha":
                if datos[i]=="default":
                    datos[i]=(f"1885-1-1:{datetime.now().strftime('%Y-%m-%d')}")
                else:
                    datos[i]=(f"1885-1-1:{datos[i]}")
            elif i =="precio":
                if datos[i]=="default":
                    datos[i]=(f"0-{precio['precio_original__max']}")
                elif datos[i]=="+20001€":
                    datos[i]=(f"20001-{precio['precio_original__max']}")
                else:
                    datos[i]=str(datos[i]).replace("€","")
            elif i =="kilometros":
                if datos[i]=="default":
                    datos[i]=(f'0-{kilometros_max["kilometros__max"]}')
                elif datos[i]=="+100001Km":
                    datos[i]=(f'100001-{kilometros_max["kilometros__max"]}')
                datos[i]=(f'{str(datos[i]).replace("Km","")}')
            elif datos[i]=="default":     
                datos[i]=""
            logs("log_fecha.txt",str(datos["fecha"]))

        resultado=Coche.objects.filter(
            Q(modelo__nombre__icontains=datos["modeloselect"]) &
            Q(modelo__marca__nombre__icontains=datos["marcaselect"]) &
            Q(fecha_matriculacion__lte=datos["fecha"].split(":")[1]) &
            Q(fecha_matriculacion__gte=datos["fecha"].split(":")[0]) &
            Q(tipo__tipo__icontains=datos["tipo"]) &
            Q(cambio__icontains=choices_search(datos["cambio"],CAMBIO_CHOICES)) &
            Q(kilometros__gte=datos["kilometros"].split("-")[0]) &
            Q(kilometros__lte=datos["kilometros"].split("-")[1]) &
            Q(localizacion__icontains=choices_search(datos["local"],PROVINCE_CHOICES)) &
            Q(precio_original__gte=datos["precio"].split("-")[0]) &
            Q(precio_original__lte=datos["precio"].split("-")[1]),
            )
        flag=True
        contador=len(resultado)
        paginator=Paginator(resultado,4)
        page_number=request.GET.get('page')
        resultado =paginator.get_page(page_number)
        if contador==0:
            resultado2=Coche.objects.order_by("-descuento")
            paginator=Paginator(resultado2,4)
            page_number=request.GET.get('page')
            resultado2 =paginator.get_page(page_number)
            return render(request, "inicio.html",{"fecha":datetime.now().strftime('%Y-%m-%d'),"resultado":resultado2,"filtro":Coche.objects.all(),"marca":marca, "modelo":modelo, "tipos":tipos, "contador":contador,"provincia":provincia, "cambios":cambios,"flag":flag})
        

        logs("log_diccionario",str(datos))
        return render(request, "inicio.html",{"fecha":datetime.now().strftime('%Y-%m-%d') ,"resultado":resultado, "filtro":Coche.objects.all(),"marca":marca, "modelo":modelo, "tipos":tipos, "contador":contador,"provincia":provincia, "cambios":cambios,"flag":flag,})


      
def logs(file="log",mensaje=""):
    escribir = open(file, "a")
    escribir.write(mensaje+"\n")
    escribir.close()

def choices_search(search="",lista_choise=list()):
    
    if search=="":
        return ""
    for i in lista_choise:
        if i[1]==search:
            return i[0]


"""def delete_dic(dic):
    logs("log_dic2.txt",str(dic))
    for i in dic:
        logs("log_dic2.txt",str(i))"""
def lista_fuc(lista=list()):
    lista=list(lista)
    lista_datos=list()
    for i in range(len(lista)):
        lista_datos.append(lista[i][1])
        
    lista_tupla=tuple(lista_datos)
    return lista_tupla