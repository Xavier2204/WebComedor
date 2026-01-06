from django.contrib import admin
from .models import Attendance # Importa el modelo desde la misma app

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    # Columnas que verás en la lista de asistencias
    list_display = ('beneficiary', 'fecha', 'observaciones')
    
    # Filtro lateral para buscar por fecha o por un niño específico
    list_filter = ('fecha', 'beneficiary')
    
    # Buscador para encontrar al niño por nombre o apellido
    # El doble guion bajo (__) permite buscar en el modelo relacionado
    search_fields = ('beneficiary__nombre', 'beneficiary__apellidos')
    
    # La fecha es automática, así que la ponemos como solo lectura
    readonly_fields = ('fecha',)