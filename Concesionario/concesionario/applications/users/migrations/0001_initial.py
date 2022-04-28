# Generated by Django 4.0.4 on 2022-04-28 09:57

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('almacen', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario_Registrado',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('dni', models.CharField(max_length=9, primary_key=True, serialize=False, unique=True, verbose_name='DNI')),
                ('nombre', models.CharField(max_length=25, verbose_name='Nombre')),
                ('primer_apellido', models.CharField(max_length=50, verbose_name='1ºApellido')),
                ('segundo_apellido', models.CharField(max_length=50, verbose_name='2ºApellido')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Correo Electrónico')),
                ('username', models.CharField(max_length=20, unique=True, verbose_name='Username')),
                ('passw', models.CharField(max_length=200, verbose_name='Password')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('is_staff', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Usuario_Concesionario',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('dni', models.CharField(max_length=9, primary_key=True, serialize=False, unique=True, verbose_name='DNI')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('nombre', models.CharField(max_length=25, verbose_name='Nombre')),
                ('primer_apellido', models.CharField(max_length=50, verbose_name='1ºApellido')),
                ('segundo_apellido', models.CharField(max_length=50, verbose_name='2ºApellido')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Correo Electrónico')),
                ('username', models.CharField(max_length=20, unique=True, verbose_name='Username')),
                ('passw', models.CharField(max_length=200, verbose_name='Password')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('concesionario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='almacen.concesionario', verbose_name='Concesionario')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Usuario_Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=20, unique=True, verbose_name='Username')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Correo Electrónico')),
                ('passw', models.CharField(max_length=200, verbose_name='Password')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('is_staff', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]