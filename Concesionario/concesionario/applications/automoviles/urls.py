from django.urls import path
from django.contrib import admin
from . import views 

app_name = "app_automoviles"

urlpatterns =[ 
	path('',views.InicioView.as_view(),name='inicio'),
	
]

