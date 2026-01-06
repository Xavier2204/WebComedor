from django.db import models

# Create your models here.
from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50) 
    unidad_medida = models.CharField(max_length=20)
    cantidad_actual = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cantidad_minima = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.nombre

class MovimientoInventario(models.Model):
    TIPO_CHOICES = [('ENTRADA', 'Entrada'), ('SALIDA', 'Salida')]
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='movimientos')
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)
    comentario = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if self.tipo == 'ENTRADA':
            self.producto.cantidad_actual += self.cantidad
        else:
            self.producto.cantidad_actual -= self.cantidad
        self.producto.save()
        super().save(*args, **kwargs)