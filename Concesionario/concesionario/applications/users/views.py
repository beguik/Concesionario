from django.shortcuts import render, redirect
from django.views.generic import View
#from django.contrib.auth.forms import UserCreationForm
from .forms import *
from django.contrib.auth import login
from django.contrib import messages


class Registro(View):

	def get(self,request):

		form=CreacionUser()
		formDatos=RegistroForm()
		return render(request,"registro.html",{"form":form, "formDatos":formDatos})

	def post(self,request):
		
		form=UserCreationForm(request.POST)
		formDatos=RegistroForm(request.POST,request.FILES)
		print(form)
		print(formDatos)
		if form.is_valid():

			if formDatos.is_valid():

				datos=formDatos.cleaned_data
				dni =datos['dni']
				nombre=datos['nombre']
				primer_apellido=datos['primer_apellido']
				segundo_apellido=datos['segundo_apellido']

				if validarDni(dni):
					user=form.save()

					nuevo=Usuario(usuario=user, dni=dni, nombre=nombre, primer_apellido=primer_apellido, segundo_apellido=segundo_apellido)
					nuevo.save()
				
					login(request, user)
			
					return redirect('Inicio')
				else: 
					mensaje="Compruebe que el dni sea correcto"
					return render(request,"registro.html",{"form":form,"formDatos":formDatos, "mensaje":mensaje})

		
		else:

			
			for msg in form.error_messages:
				messages.error(request,form.error_messages[msg])
			return render(request,"registro.html",{"form":form,"formDatos":formDatos})




def home(request):
	
	return render (request,"base.html", )



#Función para validar dni
def validarDni(dni):

	#tamaño máximo 9 caracteres
	if len(dni)==9:
		#extraemos los numeros
		numeros=int(dni[0:8])
		#extraemos la letra y la ponemos mayúscula
		letra=dni[8:].upper()
		#extraemo el modulo del numero entre 23
		modulo=numeros%23
		#cargamos la clave que nos servirá para validar el resultado
		clave="TRWAGMYFPDXBNJZSQVHLCKET"
		#seleccionamos la key dentro del string clave con el modulo recodio
		key=clave[modulo:modulo+1]
		#verificamos si la letra es la correcta
		if(letra!=key):
			return False
		else:
			return True