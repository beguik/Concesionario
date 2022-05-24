from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, View
from .models import *
from django.db.models import FilteredRelation, Q
from datetime import datetime, timedelta 
from django.db.models import Max
from django.core.paginator import Paginator
from .choices import *
from applications.users.models import Usuario
from django.http import HttpResponseRedirect
from applications.administracion.models import Reserva
from .forms import *


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
        respuesta=Coche.objects.all().order_by('created_at')[:50]
        paginator=Paginator(respuesta,3)
        page_number=request.GET.get('page')
        resultado =paginator.get_page(page_number)

        """
        a=Modelo.objects.filter(id_modelo__gte=146)
        a.delete()
        """        
        
        return render(request,"inicio.html",{"usuario":Usuario.objects.all(),"fecha":datetime.now().strftime('%Y-%m-%d'),"filtro":filtro,"resultado":resultado,"tipos":tipos, "provincia":provincia,"marca":marca, "modelo":modelo, "cambios":cambios,})
    
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
        logs("log_dic",datos)
        
        
        if 'modeloselect' not in datos.keys():
            datos.update({'modeloselect': ''})
        for i in datos.keys():
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
            return render(request, "inicio.html",{"usuario":Usuario.objects.all(),"fecha":datetime.now().strftime('%Y-%m-%d'),"resultado":resultado2,"filtro":Coche.objects.all(),"marca":marca, "modelo":modelo, "tipos":tipos, "contador":contador,"provincia":provincia, "cambios":cambios,"flag":flag})
        

        logs("log_diccionario",str(datos))
        return render(request, "inicio.html",{"usuario":Usuario.objects.all(),"fecha":datetime.now().strftime('%Y-%m-%d') ,"resultado":resultado, "filtro":Coche.objects.all(),"marca":marca, "modelo":modelo, "tipos":tipos, "contador":contador,"provincia":provincia, "cambios":cambios,"flag":flag})


      
def logs(file="log",mensaje=""):
    escribir = open(file+".txt", "a")
    escribir.write(str(mensaje)+"\n")
    escribir.close()

def choices_search(search="",lista_choise=list()):
    a,b = 'áéíóúüñÁÉÍÓÚÜÑ','aeiouunAEIOUUN'
    trans = str.maketrans(a,b)
    if search=="":
        return ""
    for i in lista_choise:
        if i[1].translate(trans)==search:
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
class Info_coche(View):
    model=Coche
    def get(self,request,pk):
        coche=Coche.objects.get(matricula=pk)
        
        logs("log_pk",pk)
        return render(request,"coche/info.html",{"provincia":lista_fuc(PROVINCE_CHOICES),"usuario":Usuario.objects.all(),"coche":coche})
#CONFIRMACION RESERVA
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
                usuario_registro = usuario,
                coche = coche,
                fecha_inicio_reserva = fecha_inicio,
                fecha_fin_reserva = fecha_fin,
            )

            success_url = reverse_lazy('app_automoviles:inicio')
            return HttpResponseRedirect(success_url)
        else:
            success_url = reverse_lazy('app_automoviles:inicio')
            return HttpResponseRedirect(success_url)



#CSV
import csv, io
from django.shortcuts import render
from django.contrib import messages
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
            logs("log_keys_datos",datos.keys())
            if "matricula" not in datos.keys():
                if request.FILES["file"].name=="coche.csv":
                    
                    leer_split2=list()
                    keys=list()
                    resultado=list()
                    dic_suport=dict()
                    
                    a,b = 'áéíóúüñÁÉÍÓÚÜÑ','aeiouunAEIOUUN'
                    trans = str.maketrans(a,b)
                    leer=request.FILES["file"].read().decode("utf-8").translate(trans).lower()
                    leer_split1=leer.split("\r\n")
                    f=open(f"coche_{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}_{datos['usu']}.csv","w")
                    f.write(leer)
                    f.close()
                    
                            
                    for i in leer_split1:
                        leer_split2.append(i.split(";"))
                    for key in leer_split2[0]:                        
                        keys.append(key)
                        logs("log_keys", keys)
                    leer_split2.pop(0)
                    resultado_validacion=keys_comprobacion_csv(keys,leer_split2)
                    diccionario_resultado=dict()
                    
                    contar=0
                    if resultado_validacion[0]:
                        diccionario_resultado=resultado_validacion[2]
                        a,b = 'aeiouunAEIOUUN','áéíóúüñÁÉÍÓÚÜÑ'
                        trans2 = str.maketrans(a,b)
                        logs("logs_diccionario_resultado", diccionario_resultado)
                        
                        for dic in diccionario_resultado:
                            
                            contar=contar+1
                            try:
                                
                                if Marca.objects.filter(nombre=dic["marca"]).exists() or Marca.objects.filter(nombre=dic["marca"].title()).exists() or Marca.objects.filter(nombre=dic["marca"].upper()).exists():
                                    logs("logs_cuentamarcas",dic)
                                    logs("log_bool_modelo",str(contar)+str(Modelo.objects.filter(nombre=dic["modelo"].title()).exists()))
                                    if not Modelo.objects.filter(nombre=dic["modelo"]).exists() and not Modelo.objects.filter(nombre=dic["modelo"].title()).exists() and not Modelo.objects.filter(nombre=dic["modelo"].upper()).exists():
                                        logs("logs_punto1","1")

                                        marca_objeto=Marca.objects.get(nombre=dic["marca"].title())

                                        if not marca_objeto:
                                            marca_objeto=Marca.objects.get(nombre=dic["marca"].upper())
                                        if not marca_objeto:
                                             marca_objeto=Marca.objects.get(nombre=dic["marca"])
                                        
                                        modelo_obj = Modelo.objects.create(
                                        nombre=dic["modelo"].title(),
                                        marca=marca_objeto,
                                        )
                                    else:
                                        logs("logs_modelos_quiero_terminar",dic["modelo"].capitalize())
                                        modelo_obj=Modelo.objects.get(nombre=dic["modelo"].title())
                                        if not modelo_obj:
                                            
                                            modelo_obj=Modelo.objects.get(nombre=dic["modelo"].upper())
                                        if not modelo_obj:
                                            modelo_obj=Modelo.objects.get(nombre=dic["modelo"])
                                        
                                        
                                    
                                    tipo_obj=TiposCoches.objects.get(tipo=dic["tipo"].title())
                                    if not tipo_obj:
                                        tipo_obj=TiposCoches.objects.get(nombre=dic["tipo"])
                                    localizacion_para_crear=choices_search(dic["localizacion"].title().translate(trans),PROVINCE_CHOICES)
                                    garantia_para_crear=choices_search(dic["garantia"].replace("m","M"),GARANTIA_CHOICES)
                                    puertas_para_crear=choices_search(str(dic["puertas"]).title(),PUERTAS_CHOICES)
                                    cambio_para_crear=choices_search(dic["cambio"].title(),CAMBIO_CHOICES)
                                    if not dic["imagen"]:
                                        dic["imagen"]="coche/sinimagen.jpg"
                                    if localizacion_para_crear and garantia_para_crear and puertas_para_crear and cambio_para_crear:
                                        
                                        coche_objeto = Coche.objects.create(
                                            matricula=dic["matricula"],
                                            modelo=modelo_obj,
                                            precio_original=dic["precio"],
                                            descuento=dic["descuento"],
                                            localizacion=localizacion_para_crear,
                                            tipo=tipo_obj,
                                            kilometros=dic["kilometros"],
                                            fecha_matriculacion=dic["fecha matriculacion"],
                                            potencia=dic["potencia"],
                                            descripcion=dic["descripcion"],
                                            garantia=garantia_para_crear,
                                            puertas=puertas_para_crear,
                                            cambio=cambio_para_crear,
                                            imagen=dic["imagen"],
                                        )
                                    else:
                                        if not localizacion_para_crear:
                                            resultado_validacion[1].append(
                                                f"La localización esta incorrecta en la linea {contar}"
                                            )
                                        elif not garantia_para_crear:
                                            resultado_validacion[1].append(
                                                f"La garantía esta incorrecta en la linea {contar}"
                                            )
                                        elif not puertas_para_crear:
                                            resultado_validacion[1].append(f"La puerta esta incorrecta en la linea {contar}")
                                        elif not cambio_para_crear:
                                            resultado_validacion[1].append(f"El cambio esta incorrecto en la linea {contar}")
                                else:
                                    resultado_validacion[1].append(
                                        f"La marca {dic['marca']} no existe.")
                            except Exception as e:
                                resultado_validacion[1].append(
                                        f"Error inesperado en la linea {contar} con el error {e}")

                       
                        
                        

                    
                    return render(request, "coche/add.html",{"errores":resultado_validacion[1],"usuario":usuario,"form":form,"marca":marca,"modelo":modelo,"fecha":fecha,"tipos":tipos, "diccionario_values": diccionario_resultado})
                elif request.FILES:
                    lista_no_csv=list()
                    if request.FILES["file"].name.endswith("csv"):
                        
                        lista_no_csv.append("El archivo no es un csv")
                    else:
                        lista_no_csv.append("El nombre del archivo no es correcto. Debe ser coche.csv")
                    return render(request, "coche/add.html",{"errores":lista_no_csv,"usuario":usuario,"form":form,"marca":marca,"modelo":modelo,"fecha":fecha,"tipos":tipos})
            else:
                datos=request.POST
                logs('log_datos', datos)
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
#Comprobaciones csv_file
def keys_comprobacion_csv(keys,lista):
    verificacion=True
    mensaje=list()
    lista_dic=dict()
    if len(keys)==15:
        for keys_comprobacion_number in range(len(KEY_CHOICES)):
            if KEY_CHOICES[keys_comprobacion_number] != keys[keys_comprobacion_number]:
                verificacion=False
                mensaje.append("En el encabezado hay una palabra que no coincide con:")
                mensaje.append("matrícula, marca, modelo, precio, descuento, localización, tipo, kilómetros, fecha matriculación, potencia, garantía, puertas, cambio, imagen, descripción")
                break
    elif len(keys)>15:
        verificacion=False
        mensaje.append("El encabezado tiene más valores de lo normal")
    elif len(keys)<15:
        verificacion=False
        mensaje.append("El encabezado tiene menos valores de lo normal")
    if verificacion:
        for i in range(len(lista[:-1])):
            
            if len(keys)!=len(lista[i]):
                verificacion=False
                mensaje.append("Hubo un error en la linea: "+str(i+1))
    # Poner lista de lineas y ponerlo separado por comasn en el mensaje
    if verificacion:
        lista_dic=diccionario( lista[:-1], keys)
        logs("log_lista_dic", len(lista_dic))
        for i in range(len(lista_dic)):
            if not validarMatricula(lista_dic[i]["matricula"]):
                verificacion=False
                mensaje.append(f"Matricula: {lista_dic[i]['matricula']} no es correcta\n")
            if not validarKilometros(lista_dic[i]["kilometros"]):
                verificacion=False
                mensaje.append(f"Kilometros: {lista_dic[i]['kilometros']} no es correcta\n")
            if not validarPotencia(lista_dic[i]["potencia"]):
                verificacion=False
                mensaje.append(f"Potencia: {lista_dic[i]['potencia']} no es correcta\n")
            if not validarPrecio(lista_dic[i]["precio"]):
                verificacion=False
                mensaje.append(f"Precio: {lista_dic[i]['precio']} no es correcta\n")
            if not validarDescuento(lista_dic[i]["descuento"]):
                verificacion=False
                mensaje.append(f"Descuento: {lista_dic[i]['descuento']} no es correcta\n")
        # Poner sistemas de lineas de error 
    logs("log_verificacion",mensaje)
    return [verificacion,mensaje,lista_dic]
        
        
    
def diccionario( leer_split2, keys):
    dic_suport=dict()
    resultado=list()
    logs("logs_split2",leer_split2)
    for i in leer_split2:
        if len(keys)==len(i):
            
                for number in range(len(keys)):                                        
                    logs("log_number",keys)
                    logs("log_number2", number)
                    dic_suport[keys[number]]=i[number]
                                        
                resultado.append(dic_suport.copy())
    logs("log_resultado", resultado)
    return resultado