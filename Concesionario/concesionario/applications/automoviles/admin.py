from django.contrib import admin
from .models import *

class MarcaAdmin(admin.ModelAdmin):
    list_display = (
        'id_marca',
        'nombre',
        'created_at',
        'updated_at',
    )

    search_fields = ('nombre',)

    list_filter = ('nombre','created_at','updated_at',)

admin.site.register(Marca, MarcaAdmin)


class ModeloAdmin(admin.ModelAdmin):
    list_display = (
        'id_modelo',
        'nombre',
        'marca',
        'created_at',
        'updated_at',
    )

    search_fields = ('nombre',)

    list_filter = ('nombre','marca','created_at','updated_at',)

admin.site.register(Modelo, ModeloAdmin)


class CocheAdmin(admin.ModelAdmin):
    list_display = (
        'matricula',
        'modelo',
        'precio_original',
        'descuento',
        'precio_final',
        'localizacion',
        'tipo',
        'kilometros',
        'fecha_matriculacion',
        'potencia',
        'descripcion',
        'garantia',
        'puertas',
        'cambio',
        'reservado',
        'vendido',
        'dado_de_baja',
        'created_at',
        'updated_at',
        'imagen',
    )

    search_fields = ('matricula',)

    list_filter = ('modelo','reservado','localizacion','potencia','dado_de_baja','created_at','updated_at',)

admin.site.register(Coche, CocheAdmin)

class TiposAdmin(admin.ModelAdmin):
    list_display = (
        'id_tipo_coche',
        'tipo',
    )

    search_fields = ('tipo',)

admin.site.register(TiposCoches, TiposAdmin)
