from django.urls import path
from django.contrib import admin
from .views import Registro
from . import views 

app_name = "app_usuarios"

urlpatterns =[ 
	path('registro/', Registro.as_view(), name="registro"),
	path('', views.home, name="Inicio"),
	path('login/', views.SignInView.as_view(), name='login'),
    path('logout/', views.SignOutView.as_view(), name='logout'),
    path('perfil/', views.Perfil.as_view(), name='perfil'),
	
]