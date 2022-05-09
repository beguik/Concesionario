from django.urls import path
from django.contrib import admin
from .views import Registro
from . import views 

app_name = "app_usuarios"

urlpatterns =[ 
	
	
	
	path('registro/', views.Registro.as_view(), name="registro"),
	path("login_cert/",views.cert,name="login_cert"),
	path('login/', views.SignInView.as_view(), name='login'),
    path('logout/', views.SignOutView.as_view(), name='logout'),
    path('perfil/', views.Perfil.as_view(), name='perfil'),
	
]