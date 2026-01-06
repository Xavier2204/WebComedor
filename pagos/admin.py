from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import PagoCuota

@admin.register(PagoCuota)
class PagoCuotaAdmin(admin.ModelAdmin):
    list_display = ('beneficiary', 'monto', 'mes_correspondiente', 'fecha_pago')
    list_filter = ('mes_correspondiente', 'metodo')
    search_fields = ('beneficiary__nombre', 'beneficiary__apellidos')