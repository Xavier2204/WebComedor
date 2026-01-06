from django.db import models

# Create your models here.
from django.db import models
from beneficiarios.models import Beneficiary # Importas el modelo de la otra app

class Attendance(models.Model):
    beneficiary = models.ForeignKey(
        Beneficiary, 
        on_delete=models.CASCADE, 
        related_name='asistencias'
    )
    fecha = models.DateField(auto_now_add=True, verbose_name="Fecha")
    llego_puntual = models.BooleanField(default=True, verbose_name="¿Asistió?")
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Asistencia"
        verbose_name_plural = "Asistencias"
        # Evita que se registre al mismo niño dos veces el mismo día
        unique_together = ('beneficiary', 'fecha') 

    def __str__(self):
        return f"{self.beneficiary} - {self.fecha}"