from django import forms
from .models import *

class DateTimeInput (forms.DateTimeInput):
	input_type='date'

class TexArea(forms.Textarea):
	input_type="texarea"


class AñadirCoche(forms.ModelForm):
	class Meta: 
		model= Coche
		fields=['matricula', 
				'precio_original',
				'descuento',
				'localizacion',
				'modelo',
				'tipo',
				'kilometros',
				'fecha_matriculacion',
				'potencia',
				'descripcion',
				'garantia',
				'puertas',
				'cambio',
				'imagen',
				]

		widgets={
				'descripcion':TexArea(),
				'fecha_matriculacion':DateTimeInput(attrs={'class':'form-control'}),
				
				}

		labels ={
				'matricula:Matrícula', 
				'precio_original:Precio',
				'descuento:Descuento',
				'localizacion:Localización',
				'tipo:Tipo',
				'kilometros:Kilómetros',
				'fecha_matriculacion:fecha',
				'potencia:Caballos de Potencia',
				'descripcion:Descripción',
				'garantia:Garantía',
				'puertas:Puertas',
				'cambio:Tipo de Cambio',
				'imagen:Imagen',	
		}





