from django.db import models

# Create your models here.
from django.db import models

class Transaccion(models.Model):
    TIPO = [
        ('INGRESO', 'Ingreso (+)'),
        ('EGRESO', 'Egreso (-)'),
    ]
    CATEGORIAS = [
        ('ALIMENTOS', 'Compra de Alimentos'),
        ('DONACION', 'Donación Recibida'),
        ('SERVICIOS', 'Servicios Básicos (Luz/Agua/Gas)'),
        ('SUELDOS', 'Sueldos/Limpieza'),
        ('OTROS', 'Otros'),
    ]

    tipo = models.CharField(max_length=10, choices=TIPO)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    descripcion = models.CharField(max_length=255, verbose_name="Detalle del gasto/ingreso")
    fecha = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Transacción"
        verbose_name_plural = "Contabilidad (Ingresos y Egresos)"

    def __str__(self):
        return f"{self.tipo} - {self.descripcion} (${self.monto})"