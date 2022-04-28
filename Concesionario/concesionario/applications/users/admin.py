from django.contrib import admin
from .models import *

class AdminAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'passw',
        'created_at',
        'updated_at',
        'is_staff',
    )

    search_fields = ('username',)

    list_filter = ('is_staff',)

admin.site.register(Usuario_Admin, AdminAdmin)

class Normal_UserAdmin(admin.ModelAdmin):
    list_display = (
        'dni',
        'username',
        'email',
        'passw',
        'nombre',
        'primer_apellido',
        'segundo_apellido',
        'created_at',
        'updated_at',
    )

    search_fields = ('username','dni')

    list_filter = ('is_staff',)

admin.site.register(Usuario_Registrado, Normal_UserAdmin)

class Concesionario_UserAdmin(admin.ModelAdmin):
    list_display = (
        'dni',
        'concesionario',
        'username',
        'email',
        'passw',
        'nombre',
        'primer_apellido',
        'segundo_apellido',
        'phone',
        'created_at',
        'updated_at',
    )

    search_fields = ('username','dni')

    list_filter = ('is_staff','concesionario',)

admin.site.register(Usuario_Concesionario, Concesionario_UserAdmin)