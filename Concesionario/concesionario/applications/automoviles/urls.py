from django.urls import path
from django.contrib import admin
from . import views 

app_name = "app_automoviles"

urlpatterns =[ 
	
	path("",views.Inicio.as_view(),name="inicio"),
	path("add/",views.Add.as_view(),name="add"),
	path("info/<pk>",views.Info_coche.as_view(),name="info"),
    path('confirmar_reserva/<pk>/', views.ReservaView.as_view(), name='confirmar_reserva'),

]

