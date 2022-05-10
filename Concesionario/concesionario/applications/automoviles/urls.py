from django.urls import path
from django.contrib import admin
from . import views 

app_name = "app_automoviles"

urlpatterns =[ 
	path('',views.InicioView.as_view(),name='inicio'),
	path("inicio2/",views.Inicio_v2.as_view(),name="Inicio_v2"),
	
	
]

