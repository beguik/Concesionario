# Generated by Django 4.0.4 on 2022-05-09 08:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('almacen', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dni', models.CharField(max_length=9, unique=True, verbose_name='DNI')),
                ('nombre', models.CharField(max_length=25, verbose_name='Nombre')),
                ('primer_apellido', models.CharField(max_length=50, verbose_name='1ºApellido')),
                ('segundo_apellido', models.CharField(max_length=50, verbose_name='2ºApellido')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None)),
                ('concesionario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='almacen.concesionario', verbose_name='Concesionario')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
