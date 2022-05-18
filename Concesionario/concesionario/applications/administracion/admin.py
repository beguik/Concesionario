from django.contrib import admin
from .models import *
from applications.users.models import *


class CargaAdmin(admin.ModelAdmin):
    list_display = (
        'id_cargas',
        'get_usuario',
        'coche',
        'created_at',
        'updated_at',
    )

    search_fields = ('usuario_concesionario','coche')

    list_filter = ('coche','created_at','updated_at',)

    @admin.display(description='Usuario')
    def get_usuario(self,obj):
        return obj.usuario_concesionario.dni

admin.site.register(Carga, CargaAdmin)


class ReservaAdmin(admin.ModelAdmin):
    model=Reserva
    list_display = (
        'id_reserva',
        'get_usuario',
        'coche',
        'fecha_inicio_reserva',
        'fecha_fin_reserva',
        'created_at',
        'updated_at',
    )

    search_fields = ('usuario_registro','coche')

    list_filter = ('coche','fecha_inicio_reserva','fecha_fin_reserva',)
    @admin.display(description='Usuario')
    def get_usuario(self,obj):
        return obj.usuario_registro.dni

admin.site.register(Reserva, ReservaAdmin)