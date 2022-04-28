from django.contrib import admin
from .models import Concesionario

class ConcesionarioAdmin(admin.ModelAdmin):
    list_display = (
        'id_concesionario',
        'nombre',
        'created_at',
        'updated_at',
    )

    search_fields = ('nombre',)

    list_filter = ('nombre','created_at','updated_at',)

admin.site.register(Concesionario, ConcesionarioAdmin)
