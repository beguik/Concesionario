from django.contrib import admin
from .models import *


class CargaAdmin(admin.ModelAdmin):
    list_display = (
        'id_cargas',
        'usuario_concesionario',
        'coche',
        'created_at',
        'updated_at',
    )

    search_fields = ('usuario_concesionario','coche')

    list_filter = ('usuario_concesionario','coche','created_at','updated_at',)

admin.site.register(Carga, CargaAdmin)


class ReservaAdmin(admin.ModelAdmin):
    list_display = (
        'id_reserva',
        'usuario_registro',
        'coche',
        'fecha_inicio_reserva',
        'fecha_fin_reserva',
        'created_at',
        'updated_at',
    )

    search_fields = ('usuario_registro','coche')

    list_filter = ('usuario_registro','coche','fecha_inicio_reserva','fecha_fin_reserva',)

admin.site.register(Reserva, ReservaAdmin)
