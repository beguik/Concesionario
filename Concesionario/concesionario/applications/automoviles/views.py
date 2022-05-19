from django.shortcuts import render
from django.views.generic import TemplateView, ListView, View
from django.db.models import FilteredRelation, Q
from django.db.models import Max
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
from datetime import datetime, timedelta 
from applications.users.models import Usuario
from applications.administracion.models import Reserva
from .choices import *
from .models import *
from .forms import *
import collections
import hashlib
import csv, io


class Inicio(View):
    model=Coche

    def get(self,request):
        
        marca=Marca.objects.all()
        modelo=Modelo.objects.all()
        filtro=Coche.objects.all()
        tipos=TiposCoches.objects.all() 
        provincia= lista_fuc(PROVINCE_CHOICES)
        cambios= lista_fuc(CAMBIO_CHOICES)
        respuesta=Coche.objects.all().order_by('created_at')[:50]
        paginator=Paginator(respuesta,3)
        page_number=request.GET.get('page')
        resultado =paginator.get_page(page_number)
        usuario=Usuario.objects.all()
        
        
        return render(request,"inicio.html",{"fecha":datetime.now().strftime('%Y-%m-%d'),"filtro":filtro,"resultado":resultado,"tipos":tipos, "provincia":provincia,"marca":marca, "modelo":modelo, "cambios":cambios,"usuario":usuario})
    
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
        usuario=Usuario.objects.all()

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
            ).order_by('created_at')[:50]
        flag=True
        contador=len(resultado)
        paginator=Paginator(resultado,3)
        page_number=request.GET.get('page')
        resultado =paginator.get_page(page_number)
        if contador==0:
            resultado2=Coche.objects.order_by("-descuento")[:50]
            paginator=Paginator(resultado2,3)
            page_number=request.GET.get('page')
            resultado2 =paginator.get_page(page_number)
            return render(request, "inicio.html",{"fecha":datetime.now().strftime('%Y-%m-%d'),"resultado":resultado2,"filtro":Coche.objects.all(),"marca":marca, "modelo":modelo, "tipos":tipos, "contador":contador,"provincia":provincia, "cambios":cambios,"flag":flag,"usuario":usuario})
        

        logs("log_diccionario",str(datos))
        return render(request, "inicio.html",{"fecha":datetime.now().strftime('%Y-%m-%d') ,"resultado":resultado, "filtro":Coche.objects.all(),"marca":marca, "modelo":modelo, "tipos":tipos, "contador":contador,"provincia":provincia, "cambios":cambios,"flag":flag,"usuario":usuario})


class Add(View):

    def get(self,request):
        usuario=Usuario.objects.all()
        marca=Marca.objects.all()
        modelo=Modelo.objects.all()
        tipos=TiposCoches.objects.all()
        form=AñadirCoche
        fecha=datetime.now().strftime('%Y-%m-%d') 


        return render(request, "coche/add.html",{"usuario":usuario,"form":form,"marca":marca,"modelo":modelo,"fecha":fecha,"tipos":tipos})
    
    def post(self,request):
        usuario=Usuario.objects.all()
        marca=Marca.objects.all()
        modelo=Modelo.objects.all()
        tipos=TiposCoches.objects.all()
        form=AñadirCoche
        fecha=datetime.now().strftime('%Y-%m-%d') 


        if request.method=='POST':
            datos=request.POST
            #creamos una lista que contendrá el resultado de las validaciones para poder comprobar posteriormente si todas han sido correctas
            validaciones=[]
            #creamos una lista a la que le vamos añadiendo los distintos errores para poder mostrarlos luego al usuario.
            errores=[]

            matricula=datos['matricula']
            validaciones.append(validarMatricula(matricula))
            if not (validarMatricula(matricula)):
                errores.append("El campo de la matrícula no se rellenó correctamente o ya está incluida en la base de datos.")
            
            modelo=datos['modeloselect']
            if modelo=="default":
                validaciones.append(False)
                errores.append("Debe seleccionar un modelo")
            else:
                model=Modelo.objects.get(nombre=modelo)
            
            tipo=datos['tipo']
            if tipo=="default":
                validaciones.append(False)
                errores.append("Debe seleccionar un tipo")
            else:
                tip=TiposCoches.objects.get(tipo=tipo)
            
            fecha_matriculacion=datos['fecha_matriculacion']
            descripcion=datos['descripcion']

            localizacion=datos['localizacion']
            if not localizacion.isdigit():
                #controlamos aquí que ha seleccionado algún campo(al igual que en todos los choices)
                validaciones.append(False)
                errores.append("Debe seleccionar una localidad")

            kilometros= datos['kilometros']
            validaciones.append(validarKilometros(kilometros))
            if not validarKilometros(kilometros):
                errores.append("El campo kilómetros no tiene un valor correcto")

            potencia=datos['potencia']
            validaciones.append(validarPotencia(potencia))
            if not validarPotencia(potencia):
                errores.append("El campo potencia no es correcto")

            cambio=datos['cambio']
            if not cambio.isdigit():
                validaciones.append(False)
                errores.append("Debe seleccionar un tipo de cambio")
            
            garantia=datos['garantia']
            if not garantia.isdigit():
                validaciones.append(False)
                errores.append("Debe seleccionar un tipo de garantia")
            
            puertas=datos['puertas']
            if not garantia.isdigit():
                validaciones.append(False)
                errores.append("Debe seleccionar las puertas")

            precio=datos['precio_original']
            validaciones.append(validarPrecio(precio))
            if not validarPrecio(precio):
                errores.append("El campo precio no es correcto")

            descuento=datos['descuento']
            validaciones.append(validarDescuento(descuento))
            if not validarDescuento(descuento):
                errores.append("El campo precio no es correcto")
            

            imagen=datos['imagen']
            if imagen=="":
                imagen="coche/sinimagen.jpg"

            if False in validaciones:

                return render(request, "coche/add.html",{"errores":errores,"usuario":usuario,"form":form,"marca":marca,"modelo":modelo,"fecha":fecha,"tipos":tipos})

            else:
                logs("validaciones",str(validaciones))
                Coche.objects.create(matricula=matricula, modelo=model, precio_original=precio, 
                    descuento=descuento,localizacion=localizacion,tipo=tip, kilometros=kilometros,
                    fecha_matriculacion=fecha_matriculacion,potencia=potencia,descripcion=descripcion,
                    garantia=garantia,puertas=puertas, cambio=cambio,imagen=imagen )

                success_url = reverse_lazy('app_automoviles:inicio')
                return HttpResponseRedirect(success_url)

class ReservaView(View):
    model=Coche

    def get(self,request, pk):

        usuario=Usuario.objects.all()
        coche=Coche.objects.get(matricula=pk)
        fecha=datetime.now().strftime('%Y-%m-%d')
        fecha_max=datetime.today() + timedelta(days=14)

        return render(request,"coche/confirmar_reserva.html",{"coche":coche, "fecha":fecha, "fecha_max":fecha_max.strftime('%Y-%m-%d'), "usuario":usuario,})
    
    def post(self,request,pk):
        datos=request.POST
        fecha_inicio=datos['fecha']
        usuario=datos['usu']
        if usuario!='admin':
            usuario=Usuario.objects.get(dni=usuario)

            Coche.objects.filter(matricula=pk).update(reservado=True)
            coche=Coche.objects.get(matricula=pk)
            
            fecha_fin=datetime.strptime(fecha_inicio, '%Y-%m-%d') + timedelta(days=14)
            fecha_fin=str(fecha_fin).split()[0]

            logs('log_reserva', str(usuario) +' - '+ str(coche)+' - '+ fecha_inicio+' - '+fecha_fin)

            reserva=Reserva.objects.create(
                usuario = usuario,
                coche = coche,
                fecha_inicio_reserva = fecha_inicio,
                fecha_fin_reserva = fecha_fin,
            )

            success_url = reverse_lazy('app_automoviles:inicio')
            return HttpResponseRedirect(success_url)
        else:
            success_url = reverse_lazy('app_automoviles:inicio')
            return HttpResponseRedirect(success_url)

class Info_coche(View):
    model=Coche
    def get(self,request,pk):
        coche=Coche.objects.get(matricula=pk)
        
        logs("log_pk",pk)
        return render(request,"coche/info.html",{"provincia":lista_fuc(PROVINCE_CHOICES),"usuario":Usuario.objects.all(),"coche":coche})


def prueba_csv(request):
    template = "coches/prueba_csv.html"
    data = Coche.objects.all()
    
    # GET request returns the value of the data with the specified key.
    if request.method == "GET":
        usuario=Usuario.objects.all()
        return render(request, template,{"usuario":usuario,'order': 'El orden debe ser matrícula, marca, modelo, precio, descuento, localización, tipo, kilómetros, fecha_matriculación, potencia, garantía, puertas, cambio, imagen, descripción','profiles': data  }) 
    
    csv_file = request.FILES['file']    # let's check if it is a csv file

    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'THIS IS NOT A CSV FILE')
        return render(request, template)
    else:
        datos=request.POST
        usuario_devuelve=datos['usu']
        logs('log_usuario', usuario_devuelve)
        lista=list()
        lectura=request.FILES['file'].read().decode("utf-8")
        f=open("mi_fichero.csv","w")
        f.write(lectura)
        f.close()
        lista=list()
        leer=lectura
        leer2=leer.split("\n")
        leer3=leer.split(";")
        logs("log_leer",str(leer)+' - '+str(leer2)+' - '+str(leer3))
        with open("mi_fichero.csv") as csvfile:
            logs("log_tipo_de_archivo",type(csvfile))
            reader=csv.DictReader(csvfile,delimiter=";")
            for i in reader:
                logs("log_ver_tipo_variable",type(reader))
                lista.append(i)
                logs("logs_csv_prueba2",i)
            logs("logs_lista",lista)
        
        """reader=csv.DictReader(leer,delimiter=";")
        for i in reader:
            logs("log_ver_tipo_variable",type(reader))
            lista.append(i)
            logs("logs_csv_prueba2",i)
        logs("logs_csv_prueba",type(request.FILES['file'].read().decode()))
        logs("logs_csv_3",leer)
        logs("logs_lista",lista)"""
        
        #logs("log_prueba",csv_file.read())
        dic=dict()
        lectura=request.FILES['file'].read().decode("utf-8")
        csv2=csv.DictReader(lectura,delimiter=";")
        for i in csv2:
            dic.update(i)
        logs("logs_dic_copy",dic)
        
        data_set = csv_file.read().decode('UTF-8')    
        
        # setup a stream which is when we loop through each line we are able to handle a data in a stream
        io_string = io.StringIO(data_set)
        next(io_string)
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            _, created = Coche.objects.update_or_create(
                matricula=column[0],
                #modelo__marca=column[1],
                modelo=column[2],
                precio_original=column[3],
                descuento=column[4],
                localiacion=column[5],
                tipo=column[6],
                kilometros=column[7],
                fecha_matriculacion=column[8],
                potencia=column[9],
                garantia=column[10],
                puertas=column[11],
                cambio=column[12],
                imagen=column[13],
                descripcion=column[14],
            )
        context = {}
        return render(request, template, context,{"usuario":usuario,})





#comprobamos tamaño matricula
#comprobamos que son cuatro numeros y tres letras
#comprobamos que la matricula no existe ya 
#si todo es correcto devolvemos true
def validarMatricula(matricula):

    if len(matricula)==7:
        numeros=matricula[0:4]
        letras=matricula[5:7]

        if numeros.isdigit() and isinstance(letras, str):
            contador=Coche.objects.filter(matricula=matricula).count()
            if contador==0:
                return True
            else:
                return False
        else:
            return False
    else:
        return False

#comprobamos que el numero es float y que está entre 0 y 1000000
def validarKilometros(kilometros):
    
    if (float(kilometros)>-1 and float(kilometros)<1000000):
        return True 
    else:
        return False 

#comprobamos que la potencia es entera entre 0 y 1000
def validarPotencia(potencia):

    if int(potencia)>0 and int(potencia)<1000:
         return True 
    else:
        return False
   
#comprobamos que el precio es float mayor de cero y menor de 1000000
def validarPrecio(precio):
    
    if (float(precio)>0 and float(precio)<1000000):
        return True 
    else:
        return False
    
def validarDescuento(descuento):
    
    if (float(descuento)>0 and float(descuento)<100):
        return True 
    else:
        return False
    
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

def lista_fuc(lista=list()):
    lista=list(lista)
    lista_datos=list()
    for i in range(len(lista)):
        lista_datos.append(lista[i][1])
        
    lista_tupla=tuple(lista_datos)
    return lista_tupla