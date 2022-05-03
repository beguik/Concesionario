'''from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager
from phonenumber_field.modelfields import PhoneNumberField'''



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


'''@receiver(post_save, sender=User)
def crear_usuario_admin(sender, instance, created, kwargs):
    if created:
        Usuario.objects.create(usuario=instance)'''

'''@receiver(post_save, sender=User)
def guardar_usuario_admin(sender, instance, kwargs):
    instance.usuario.save()'''



'''class Usuario_Admin(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('Username', max_length=20, unique=True)
    email = models.EmailField('Correo Electrónico', max_length=254, unique=True)
    passw = models.CharField('Password', max_length=200)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    #determina que el usuario pueda entrar al panel de administración
    is_staff = models.BooleanField(default=True)

    #identificador único a la hora de login
    USERNAME_FIELD = 'username'
    #campos requeridos no entra ni el username ni el passw porque siempre son requeridos
    REQUIRED_FIELDS = ['email',]

    objects = UserManager()

    def __str__(self):
        return self.username


class Usuario_Registrado(AbstractBaseUser):
    dni = models.CharField('DNI', max_length=9, primary_key=True, unique=True)
    nombre = models.CharField('Nombre', max_length=25)
    primer_apellido = models.CharField('1ºApellido', max_length=50)
    segundo_apellido = models.CharField('2ºApellido', max_length=50)
    email = models.EmailField('Correo Electrónico', max_length=254, unique=True)
    username = models.CharField('Username', max_length=20, unique=True)
    passw = models.CharField('Password', max_length=200)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    is_staff = models.BooleanField(default=False)

    def __str__(self):
        return self.dni + ' - ' + self.username
        

class Usuario_Concesionario(AbstractBaseUser):
    dni = models.CharField('DNI', max_length=9, primary_key=True, unique=True)
    concesionario = models.ForeignKey("almacen.Concesionario", verbose_name=("Concesionario"), on_delete=models.CASCADE)
    phone= PhoneNumberField()
    nombre = models.CharField('Nombre', max_length=25)
    primer_apellido = models.CharField('1ºApellido', max_length=50)
    segundo_apellido = models.CharField('2ºApellido', max_length=50)
    email = models.EmailField('Correo Electrónico', max_length=254, unique=True)
    username = models.CharField('Username', max_length=20, unique=True)
    passw = models.CharField('Password', max_length=200)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    is_staff = models.BooleanField(default=False)

    def __str__(self):
        return self.dni + ' - ' + self.username'''