from django.db import models
from datetime import date
from django.core.validators import MinValueValidator

# 1. MODELO REPRESENTANTE
class Representative(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre Completo")
    ci = models.CharField(max_length=20, unique=True, verbose_name="Cédula/DNI")
    nacionalidad = models.CharField(max_length=50, default="Ecuatoriana")
    empleo = models.CharField(max_length=100, blank=True, null=True, verbose_name="Ocupación/Empleo")
    ingresos = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Ingresos Mensuales",
        validators=[MinValueValidator(0.00)]
    )
    convivencia = models.CharField(max_length=100, verbose_name="Con quién vive el niño")

    class Meta:
        verbose_name = "Representante"
        verbose_name_plural = "Representantes"

    def __str__(self):
        return f"{self.nombre} (CI: {self.ci})"

# 2. MODELO BENEFICIARIO (Con lógica para el Dashboard)
class Beneficiary(models.Model):
    representative = models.ForeignKey(
        Representative, 
        on_delete=models.PROTECT, 
        related_name='representados', 
        verbose_name="Representante"
    )
    nombre = models.CharField(max_length=100, verbose_name="Nombres")
    apellidos = models.CharField(max_length=100, verbose_name="Apellidos")
    ci = models.CharField(max_length=20, unique=True, verbose_name="Cédula de Identidad")
    nacimiento = models.DateField(verbose_name="Fecha de Nacimiento")
    nacionalidad = models.CharField(max_length=50, default="Ecuatoriana")
    direccion = models.TextField(verbose_name="Dirección Domiciliaria")
    contacto = models.CharField(max_length=50, verbose_name="Teléfono de Contacto")
    monthly_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Cuota Mensual")
    active = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")

    class Meta:
        verbose_name = "Beneficiario"
        verbose_name_plural = "Beneficiarios"
        ordering = ['apellidos', 'nombre']

    @property
    def edad(self):
        if not self.nacimiento: return 0
        today = date.today()
        return today.year - self.nacimiento.year - ((today.month, today.day) < (self.nacimiento.month, self.nacimiento.day))

    # --- MÉTODOS PARA EL DASHBOARD ---
    def asistio_hoy(self):
        from asistencia.models import Attendance
        return Attendance.objects.filter(beneficiary=self, fecha=date.today()).exists()

    def tiene_pago_mes_actual(self):
        from pagos.models import PagoCuota
        meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
                "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        mes_actual = meses[date.today().month - 1]
        return PagoCuota.objects.filter(beneficiary=self, mes_correspondiente=mes_actual).exists()

    def __str__(self):
        return f"{self.apellidos} {self.nombre}"

# 3. MODELO INSCRIPCIÓN (Enrollment)
class Enrollment(models.Model):
    beneficiary = models.OneToOneField(Beneficiary, on_delete=models.CASCADE, verbose_name="Beneficiario")
    escuela = models.CharField(max_length=100, verbose_name="Institución Educativa", blank=True)
    grado = models.CharField(max_length=50, verbose_name="Grado/Curso", blank=True)

    class Meta:
        verbose_name = "Inscripción Escolar"
        verbose_name_plural = "Inscripciones Escolares"

    def __str__(self):
        return f"Inscripción de {self.beneficiary}"