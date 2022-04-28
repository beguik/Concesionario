from django.db import models

class Concesionario(models.Model):
    id_concesionario = models.AutoField('ID', unique=True, primary_key=True)
    nombre = models.CharField('Concesionario', max_length=25)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name='Concesionario'
        verbose_name_plural='Concesionarios'
        ordering=['id_concesionario']

    def __str__(self):
        return self.nombre