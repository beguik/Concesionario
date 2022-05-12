from django.db import models
from django.template.defaulttags import register 


class Marca(models.Model):
	id_marca = models.AutoField('ID', primary_key=True, unique=True)
	nombre = models.CharField('Marca', max_length=20)
	created_at = models.DateTimeField(auto_now_add=True, null=True)
	updated_at = models.DateTimeField(auto_now_add=True, null=True)

	class Meta:
		verbose_name='Marca'
		verbose_name_plural='Marcas'
		ordering=['id_marca']

	def __str__(self):
		return self.nombre

class Modelo(models.Model):
    id_modelo = models.AutoField('ID', unique=True, primary_key=True)
    nombre = models.CharField('Modelo', max_length=20)
    marca = models.ForeignKey(Marca, verbose_name=("Marca"), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name='Modelo'
        verbose_name_plural='Modelos'
        ordering=['id_modelo']

    def __str__(self):
        return self.nombre

'''creamos esta clase que en principio dijimos que iba a ser diccionario
porque entendemos que los tipos de coches pueden aumentara'''
class TiposCoches(models.Model):
    id_tipo_coche = models.AutoField('ID', unique=True, primary_key=True)
    tipo = models.CharField('Tipo', max_length=25)

    class Meta:
        verbose_name='Tipos Coche'
        verbose_name_plural='Tipos Coches'
        ordering=['id_tipo_coche']

    def __str__(self):
        return self.tipo


class Coche(models.Model):
    PUERTAS_CHOICES=(
            ('2', '2 Puertas'),
            ('3', '3 Puertas'),
            ('4', '4 Puertas'),
            ('5', '5 Puertas'),
        )

    CAMBIO_CHOICES=(
            ('0', 'Automático'),
            ('1', 'Manual'),
        )

    PROVINCE_CHOICES = ('01', 'Alaba'), ('02', 'Albacete'), ('03', 'Alicante'), ('04', 'Almería'), ('05', 'Ávila'), ('06', 'Badajoz'), ('07', 'Islas Baleares'), ('08', 'Barcelona'), ('09', 'Burgos'), ('10', 'Cáceres'), ('11', 'Cádiz'), ('12', 'Castellón'), ('13', 'Ciudad Real'), ('14', 'Córdoba'), ('15', 'A Coruña'), ('16', 'Cuenca'), ('17', 'Girona'), ('18', 'Granada'), ('19', 'Guadalajara'), ('20', 'Guipúzcoa'), ('21', 'Huelva'), ('22', 'Huesca'), ('23', 'Jaén'), ('24', 'León'), ('25', 'Lleida'), ('26', 'La Rioja'), ('27', 'Lugo'), ('28', 'Madrid'), ('29', 'Málaga'), ('30', 'Murcia'), ('31', 'Navarra'), ('32', 'Ourense'), ('33', 'Asturias'), ('34', 'Palencia'), ('35', 'Las Palmas'), ('36', 'Pontevedra'), ('37', 'Salamanca'), ('38', 'Santa Cruz de Tenerife'), ('39', 'Cantabria'), ('40', 'Segovia'), ('41', 'Sevilla'), ('42', 'Soria'), ('43', 'Tarragona'), ('44', 'Teruel'), ('45', 'Toledo'), ('46', 'Valencia'), ('47', 'Valladolid'), ('48', 'Vizcaya'), ('49', 'Zamora'), ('50', 'Zaragoza'), ('51', 'Ceuta'), ('52', 'Melilla')

    GARANTIA_CHOICES = (
        ('0', '2 Meses'),('1', '4 Meses'),
        ('2', '6 Meses'),('3', '8 Meses'),
        ('4', '10 Meses'),('5', '12 Meses'),
        ('6', '14 Meses'),('7', '16 Meses'),
        ('8', '18 Meses'),('9', '20 Meses'),
        ('10', '22 Meses'),('11', '24 Meses'),
        ('12', '28 Meses'),('13', '30 Meses'),
    )

    matricula = models.CharField('MATRICULA', unique=True, primary_key=True, max_length=7)
    modelo = models.ForeignKey(Modelo, verbose_name=("Modelo"), on_delete=models.CASCADE)
    
    precio_original = models.DecimalField('Precio Original', max_digits=13, decimal_places=6)
    descuento = models.DecimalField('Descuento', max_digits=13, decimal_places=6)    
    localizacion = models.CharField('Localización', max_length=2, choices=PROVINCE_CHOICES)
    tipo = models.ForeignKey(TiposCoches, verbose_name=("Tipo"), on_delete=models.CASCADE)
    kilometros = models.FloatField('Kilometros')
    fecha_matriculacion = models.DateField('Fecha Matriculación', auto_now=False, auto_now_add=False)
    potencia = models.FloatField('Potencia')
    descripcion = models.CharField('Descripción', max_length=1024)
    garantia = models.CharField('Garantía', max_length=2, choices=GARANTIA_CHOICES)
    puertas = models.CharField('Puertas', max_length=1, choices=PUERTAS_CHOICES)
    cambio = models.CharField('Cambio', max_length=1, choices=CAMBIO_CHOICES)
    reservado = models.BooleanField('Reservado', default=False)
    vendido = models.BooleanField('Vendido', default=False)
    dado_de_baja = models.BooleanField('Dado de baja', default=False, blank=True)
    imagen = models.ImageField('Imagen', upload_to="coche", default="coche/sinimagen.jpg",blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)

    

    def _get_importe(self):

      return self.precio_original-((self.precio_original*self.descuento)/100)

    precio_final = property(_get_importe)

    def _get_potenciaw(self):
        
        return self.potencia*745.7

    potenciaw=property(_get_potenciaw)

    @register.filter
    def get_cambio(self, key):
        return self[int(key)]


  
    class Meta:
        verbose_name='Coche'
        verbose_name_plural='Coches'
        ordering=['matricula']

    def __str__(self):
        return self.matricula