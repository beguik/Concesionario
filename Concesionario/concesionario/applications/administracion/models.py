from django.db import models


class Carga(models.Model):
    id_cargas = models.AutoField('ID', unique=True, primary_key=True)
    usuario = models.ForeignKey("users.Usuario", verbose_name=("Usuario"), on_delete=models.CASCADE, default="")
    coche = models.ForeignKey("automoviles.Coche", verbose_name=("Coche"), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name='Carga'
        verbose_name_plural='Cargas'
        ordering=['id_cargas']

    def __str__(self):
        return str(self.id_cargas) + ' - ' + str(self.coche)



class Reserva(models.Model):
    id_reserva = models.AutoField('ID', unique=True, primary_key=True)
    usuario= models.ForeignKey("users.Usuario", verbose_name=("Usuario"), on_delete=models.CASCADE, default="")
    coche = models.ForeignKey("automoviles.Coche", verbose_name=("Coche"), on_delete=models.CASCADE)
    fecha_inicio_reserva = models.DateField('Inicio Reserva', auto_now=False, auto_now_add=False, blank=True, null=True)
    fecha_fin_reserva = models.DateField('Fin Reserva', auto_now=False, auto_now_add=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name='Reserva'
        verbose_name_plural='Reservas'
        ordering=['fecha_inicio_reserva']

    def __str__(self):
        return str(self.id_reserva) + ' - ' + str(self.coche)