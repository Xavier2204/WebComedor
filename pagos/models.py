from django.db import models

# Create your models here.
from django.db import models
from beneficiarios.models import Beneficiary

class PagoCuota(models.Model):
    METODOS = [
        ('EFECTIVO', 'Efectivo'),
        ('TRANSFERENCIA', 'Transferencia'),
    ]

    beneficiary = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, verbose_name="Niño/a")
    monto = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto Pagado")
    fecha_pago = models.DateField(auto_now_add=True)
    mes_correspondiente = models.CharField(max_length=20, verbose_name="Mes que paga (ej: Enero)")
    metodo = models.CharField(max_length=20, choices=METODOS, default='EFECTIVO')
    comprobante = models.CharField(max_length=50, blank=True, null=True, verbose_name="Num. Comprobante")

    class Meta:
        verbose_name = "Pago de Cuota"
        verbose_name_plural = "Pagos de Cuotas"

    def __str__(self):
        return f"{self.beneficiary} - {self.mes_correspondiente} (${self.monto})"