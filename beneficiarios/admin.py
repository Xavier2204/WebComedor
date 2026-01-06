from django.contrib import admin
from .models import Representative, Beneficiary, Enrollment
from asistencia.models import Attendance # Importación vital

# --- 1. CONFIGURACIÓN DE INLINES ---

class EnrollmentInline(admin.StackedInline):
    model = Enrollment
    extra = 1

class BeneficiaryInline(admin.TabularInline):
    model = Beneficiary
    extra = 1

class AttendanceInline(admin.TabularInline):
    model = Attendance
    extra = 0
    readonly_fields = ('fecha',)
    can_delete = False

# --- 2. REGISTRO DE MODELOS ---

@admin.register(Representative)
class RepresentativeAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ci', 'empleo', 'ingresos')
    search_fields = ('nombre', 'ci')
    inlines = [BeneficiaryInline]

@admin.register(Beneficiary)
class BeneficiaryAdmin(admin.ModelAdmin):
    # Fusionamos todas las propiedades en este único bloque
    list_display = ('apellidos', 'nombre', 'ci', 'edad', 'active')
    list_filter = ('active',)
    search_fields = ('apellidos', 'ci')
    
    # Aquí unimos los dos Inlines: Escuela y Asistencias
    inlines = [EnrollmentInline, AttendanceInline]

# Nota: Enrollment no necesita register propio si ya lo manejas como Inline, 
# pero si quieres verlo por separado, puedes descomentar la siguiente línea:
# admin.site.register(Enrollment)