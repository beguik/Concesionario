from django.contrib import admin
from .models import *

class UsuarioAdmin(admin.ModelAdmin):
   
    list_display = (

        'usuario',
        
        
    )

    search_fields = ('username',)

  

admin.site.register(Usuario, UsuarioAdmin)

