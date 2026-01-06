from django.contrib import admin
from .models import Transaccion

@admin.register(Transaccion)
class TransaccionAdmin(admin.ModelAdmin):
    # 1. Campos visibles en la tabla principal
    list_display = ('fecha', 'tipo', 'categoria', 'monto', 'descripcion')
    
    # 2. Filtros y Buscador
    list_filter = ('tipo', 'categoria', 'fecha')
    search_fields = ('descripcion', 'monto')

    # 3. OBLIGATORIO: Si el modelo tiene auto_now_add=True, 
    # la fecha DEBE ser readonly, de lo contrario el Admin da error al guardar.
    readonly_fields = ('fecha',)

    # 4. Organización de los campos en el formulario de edición
    fieldsets = (
        ('Datos de la Transacción', {
            'fields': ('tipo', 'categoria', 'monto', 'descripcion')
        }),
        ('Información de Registro', {
            'fields': ('fecha',), # Aquí aparece gracias a readonly_fields
        }),
    )

    # 5. Ordenar para que lo más reciente aparezca primero
    ordering = ('-fecha',)

    # 6. Elimina el método has_change_permission a menos que quieras 
    # saltarte las reglas de grupos de Django. Por defecto, Superuser ya lo tiene.