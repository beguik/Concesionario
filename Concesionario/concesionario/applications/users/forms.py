from django import forms 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import *


class RegistroForm(forms.Form):

	dni=forms.CharField(max_length = 9)
	nombre= forms.CharField( max_length = 25)
	primer_apellido=forms.CharField(max_length = 50,)
	segundo_apellido=forms.CharField(max_length = 50,)
	email=forms.EmailField(max_length=254,)
	username=forms.CharField(max_length=20,)
	passw=forms.CharField(max_length=200)
	
