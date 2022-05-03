from django.contrib import admin
from .models import *


class CargaAdmin(admin.ModelAdmin):
    list_display = (
        'id_cargas',
        'usuario',
        'coche',
        'created_at',
        'updated_at',
    )

    search_fields = ('usuario','coche')

    list_filter = ('usuario','coche','created_at','updated_at',)

admin.site.register(Carga, CargaAdmin)


class ReservaAdmin(admin.ModelAdmin):
    list_display = (
        'id_reserva',
        'usuario',
        'coche',
        'fecha_inicio_reserva',
        'fecha_fin_reserva',
        'created_at',
        'updated_at',
    )

    search_fields = ('usuario','coche')

    list_filter = ('usuario','coche','fecha_inicio_reserva','fecha_fin_reserva',)

admin.site.register(Reserva, ReservaAdmin)
