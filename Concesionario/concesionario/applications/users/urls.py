from django.urls import path
from django.contrib import admin
from .views import Registro
from . import views 

urlpatterns =[ 
	path('registro/', Registro.as_view()),
	path('', views.home, name="Inicio"),
	
]