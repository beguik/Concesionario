from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import *
from .models import *
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView
from django.contrib import messages


class Registro(View):

	def get(self,request):

		form=CreacionUser()
		formDatos=RegistroForm()
		return render(request,"users/registro.html",{"form":form, "formDatos":formDatos})

	def post(self,request):
		
		form=CreacionUser(request.POST)
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

					if Usuario.objects.filter(dni=dni).exists():
						mensaje="El DNI introducido ya existe"
						return render(request,"users/registro.html",{"form":form,"formDatos":formDatos, "mensaje":mensaje})

					user=form.save()
					nuevo=Usuario(usuario=user, dni=dni, nombre=nombre, primer_apellido=primer_apellido, segundo_apellido=segundo_apellido)
					nuevo.save()
				
					login(request, user)
			
					return redirect('/perfil/')
				else: 
					mensaje="Compruebe que el dni sea correcto"
					return render(request,"users/registro.html",{"form":form,"formDatos":formDatos, "mensaje":mensaje})

		
		else:

			
			for msg in form.error_messages:
				messages.error(request,form.error_messages[msg])
			return render(request,"users/registro.html",{"form":form,"formDatos":formDatos})

class SignInView(LoginView):
    template_name = 'users/login.html'

class SignOutView(LogoutView):
    pass


class Perfil(ListView):
    model=Usuario
    context_object_name='usuario'
    template_name='users/perfil.html'


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


