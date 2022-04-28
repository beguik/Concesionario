from django.db import models
from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager, models.Manager):

    def _create_superuser(self, username, email, password, is_staff, is_superuser, **extra_fields):
        user = self.model(
            username=username,
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def _create_user(self, dni, nombre, apellido1, apellido2, username, email, password, is_staff, is_superuser, **extra_fields):
        user = self.model(
            dni=dni,
            nombre=nombre,
            apellido1=apellido1,
            apellido2=apellido2,
            username=username,
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def _create_conce_user(self, dni, nombre, apellido1, apellido2, username, email, concesionario, phone, password, is_staff, is_superuser,**extra_fields):
        user = self.model(
            dni=dni,
            nombre=nombre,
            apellido1=apellido1,
            apellido2=apellido2,
            username=username,
            email=email,
            concesionario=concesionario,
            phone=phone,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        return self._create_superuser(username, email, password, True, True, **extra_fields)

    def create_normal_user(self, dni, nombre, apellido1, apellido2, username, email, password=None, **extra_fields):
        return self._create_user(self, dni, nombre, apellido1, apellido2, username, email, password, False, False, **extra_fields)

    def create_concesionario_user(self, dni, nombre, apellido1, apellido2, username, email, concesionario, phone, password=None, **extra_fields):
        return self._create_conce_user(self, dni, nombre, apellido1, apellido2, username, email, concesionario, phone, password, False, False, **extra_fields)