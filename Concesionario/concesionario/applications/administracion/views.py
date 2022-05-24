from django.shortcuts import render
from .models import *
from django.views.generic import TemplateView, ListView, View
from applications.users.models import Usuario
from applications.automoviles.models import *
from django.utils.crypto import get_random_string
import random 
from applications.automoviles.choices import *
from datetime import datetime, timedelta
from random import randrange


import csv



from django.http import HttpResponseRedirect

class reservas(ListView):
    def get(self,request):
        usuario=Usuario.objects.all()
        reservas = Reserva.objects.all()
        return render(request, "administracion/listar_reservas.html", {"reservas":reservas,"usuario":usuario})

class generarCSV(ListView):
    def get(self, request):

        with open('coche.csv', 'w', newline='') as coche:
            writer = csv.writer(coche, delimiter=';')
            writer.writerow(['Matrícula', 'Marca', 'Modelo', 'Precio', 'Descuento', 'Localización', 'Tipo', 'Kilómetros', 'Fecha Matriculación', 'Potencia', 'Garantia', 'Puertas', 'Cambio', 'Imagen', 'Descripción'])
     

            d1 = datetime.strptime('1/1/1970', '%m/%d/%Y')
            d2 = datetime.strptime('1/1/2022', '%m/%d/%Y')

            marca=Marca.objects.all()
            modelo=Modelo.objects.all()
            tipo=TiposCoches.objects.all()
            marca_lista=list()
            modelo_list=list()
            tipo_list=list()
            abecedario="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            letras=str()
            imagenes={'1':"coche/cochegranate.jpg",
                '2':"coche/cochemarron.jpg",
                '3':"coche/cochenaranja.jpg",
                '4':"coche/cochenegro.jpg",
                '5':"coche/cocherojo.jpg",
                '6':"coche/cocheturquesa.jpeg",}
          

                
            for m in modelo:
                modelo_list.append(m.nombre)
                
            for t in tipo:
                tipo_list.append(t.tipo)

            dic=[]
           
            dic.append('Matricula;marca;modelo;Precio;Descuento;Localizacion;tipo;Kilometros;Fecha matriculacion;potencia;garantia;puertas;cambio;imagen;descripcion')
            for c in range(150):
                letras=''
                numero=f"{random.randint(1,9999):04d}"
                
                for i in range(3):

                    letras+=random.choice(abecedario)

                matricula=str(numero)+str(letras)
                mod=random.choice(modelo_list)
                x=Modelo.objects.filter(nombre=mod)
                mar=x[0].marca
                tip=random.choice(tipo_list)
                precio=round(random.uniform(0.001, 10000.99), 2)
                descuento=round(random.uniform(0.00, 100.00),2)
                localidad=random.choice(PROVINCE_CHOICES)
                kilometros=random.randint(0,500000)
                potencia=random.randint(1,200)
                garantia=random.choice(GARANTIA_CHOICES)
                puerta=random.choice(PUERTAS_CHOICES)
                cambio=random.choice(CAMBIO_CHOICES)
                img=imagenes[str(random.randint(1,6))]
                descripcion=str(letras)+" Estas con las letras de mi matrícula"

                time_between_dates = d2- d1
                days_between_dates = time_between_dates.days
                random_number_of_days = random.randrange(days_between_dates)
                fecha = (d1 + timedelta(days=random_number_of_days)).strftime('%Y-%m-%d')
       
                writer.writerow([matricula,str(mar),str(mod),str(precio),str(descuento),str(localidad[1]),str(tip),str(kilometros),str(fecha),str(potencia),str(garantia[1]),str(puerta[1]),str(cambio[1]),str(img),str(descripcion)])
                
                dic.append(matricula+";"+str(mar)+";"+str(mod)+";"+str(precio)+";"+str(descuento)+";"+str(localidad[1])+";"+str(tip)+";"+str(kilometros)+";"+str(fecha)+";"+str(potencia)+";"+str(garantia[1])+";"+str(puerta[0])+";"+str(cambio[1])+";"+str(descripcion))

        return render(request, "administracion/csv.html", {"dic":dic})







