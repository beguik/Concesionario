from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField


class Usuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    dni = models.CharField('DNI', max_length=9, unique=True)
    nombre = models.CharField('Nombre', max_length=25)
    primer_apellido = models.CharField('1ºApellido', max_length=50)
    segundo_apellido = models.CharField('2ºApellido', max_length=50)
    concesionario = models.ForeignKey("almacen.Concesionario", verbose_name=("Concesionario"), on_delete=models.CASCADE, blank=True, null=True)
    phone= PhoneNumberField(blank=True)

    def str(self): 
        return self.usuario.username


