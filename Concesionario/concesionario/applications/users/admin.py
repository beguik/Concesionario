from django.contrib import admin
from .models import *



class UsuarioAdmin(admin.ModelAdmin):
   
    list_display = (

        'usuario',
        'nombre',
        'primer_apellido',
        'segundo_apellido',
        'dni',
        'concesionario'
        
        
    )

    search_fields = ('username',)

  

admin.site.register(Usuario, UsuarioAdmin)

