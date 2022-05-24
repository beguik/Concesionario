from django.urls import path
from django.contrib import admin
from . import views 

app_name = "app_administracion"

urlpatterns =[ 
	
	path('reservas/', views.reservas.as_view(), name="reservas"),
	path('csv/', views.generarCSV.as_view(), name="CSV"),
]