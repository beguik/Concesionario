from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import *
from .models import *
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from .funcion_leer_certificado import *
import hashlib

#Registro
class Registro(View):

	def get(self,request):

		form=CreacionUser()
		formDatos=RegistroForm()
		return render(request,"users/registro.html",{"form":form, "formDatos":formDatos})

	def post(self,request):
		
		form=CreacionUser(request.POST)
		formDatos=RegistroForm(request.POST,request.FILES)
		if form.is_valid():
			print(form)
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
					print(user)
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

#Registro con certificado
def cert(request):
	cert=request.GET.get('cert')
	if cert:
		diccionario_del_certificado=bien_ordenado_diccionario(resultado(certificado_en_base64(cert)))
		escribir = open("log_reques.txt", "a")
		escribir.write(str(Usuario.objects.filter(dni=diccionario_del_certificado["DNI"]).exists())+"\n")
		escribir.close()
		if Usuario.objects.filter(dni=diccionario_del_certificado["DNI"]).exists():
			respuesta=Usuario.objects.get(dni=diccionario_del_certificado["DNI"])
			login(request, respuesta.usuario)
			return redirect('/perfil/')
		else:
			form = CreacionUser(request.POST)
			formDatos = RegistroForm()
			apellido1,apellido2=diccionario_del_certificado["Apellido"].split()
			return render(request,"users/register_cert.html",{"form":form,"formDatos": formDatos,"Nombre":diccionario_del_certificado["Nombre"],"apellido1":apellido1,"apellido2":apellido2,"DNI":diccionario_del_certificado["DNI"],"password":hashlib.md5(cert.encode()).hexdigest()})
	
	else:
		form = CreacionUser()
		formDatos = RegistroForm()
		formDatos = RegistroForm(request.GET, request.FILES)
		if True:
			escribir = open("log_reques2.txt", "a")
			escribir.write(str("snsdvd")+" "+str("vdsvd")+"\n")
			escribir.close()
			if formDatos.is_valid():

				datos = formDatos.cleaned_data
				dni = datos['dni']
				nombre = datos['nombre']
				primer_apellido = datos['primer_apellido']
				segundo_apellido = datos['segundo_apellido']

				if validarDni(dni):
					if Usuario.objects.filter(dni=dni).exists():
						mensaje = "El DNI introducido ya existe"
						return render(request, "users/registro.html", {"form": form, "formDatos": formDatos, "mensaje": mensaje})

					user = form.save()
					#user.save()

					nuevo = Usuario(usuario=user, dni=dni, nombre=nombre,
					                primer_apellido=primer_apellido, segundo_apellido=segundo_apellido)
					nuevo.save()


					print(request)
					login(request, user)

					return redirect('/perfil/')
		return render(request, "users/login_cert.html")
	
#Inicio Sesion
class SignInView(LoginView):
    template_name = 'users/login.html'

#CerrarSesion
class SignOutView(LogoutView):
    pass

#PerfilUsuario
class Perfil(ListView):
    model=Usuario
    context_object_name='usuario'
    template_name='users/perfil.html'



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


