from django.urls import path
from django.contrib import admin
from . import views 

app_name = "app_automoviles"

urlpatterns =[ 
	
	path("",views.Inicio.as_view(),name="inicio"),
	
	
]

