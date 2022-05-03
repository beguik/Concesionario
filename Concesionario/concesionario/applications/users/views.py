from django.shortcuts import render, redirect
from .forms import *

def registro(request):

	form=RegistroForm(request.POST, request.FILES)
	print(form)


	return render (request,"registro.html",{"form":form} )