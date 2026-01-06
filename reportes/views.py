from django.shortcuts import render
from django.utils import timezone
from django.db.models import Sum

# Importaciones sincronizadas con tus modelos reales
from beneficiarios.models import Beneficiary
from asistencia.models import Attendance
from pagos.models import PagoCuota
from contabilidad.models import Transaccion

def reporte_mensual_integral(request, year=None, month=None):
    # 1. Parámetros de fecha
    ahora = timezone.now()
    y = int(year) if year else ahora.year
    m = int(month) if month else ahora.month
    
    meses_nombres = {
        1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 
        5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto", 
        9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
    }
    nombre_mes = meses_nombres.get(m, "Mes Desconocido")

    # 2. Procesar datos por Beneficiario
    beneficiarios = Beneficiary.objects.filter(active=True)
    listado_completo = []

    for b in beneficiarios:
        # Asistencia: Usamos el campo 'fecha' y 'llego_puntual' de tu modelo
        asistencias_count = Attendance.objects.filter(
            beneficiary=b, 
            fecha__year=y, 
            fecha__month=m, 
            llego_puntual=True
        ).count()
        
        # Pagos: Usamos el modelo 'PagoCuota' y su campo 'fecha_pago'
        pagos_mensuales = PagoCuota.objects.filter(
            beneficiary=b, 
            fecha_pago__year=y, 
            fecha_pago__month=m
        ).aggregate(total=Sum('monto'))['total'] or 0

        listado_completo.append({
            'nombre': f"{b.nombre} {b.apellidos}",
            'ci': b.ci,
            'asistencias': asistencias_count,
            'porcentaje': (asistencias_count / 20) * 100 if asistencias_count > 0 else 0,
            'cuota_mensual': b.monthly_fee,
            'pago_realizado': pagos_mensuales,
            'saldo': b.monthly_fee - pagos_mensuales
        })

    # 3. Contabilidad General (Modelo Transaccion)
    # Filtramos por tipo 'INGRESO' y 'EGRESO' según tus CHOICES
    totales_contabilidad = Transaccion.objects.filter(fecha__year=y, fecha__month=m)
    
    ingresos_extra = totales_contabilidad.filter(tipo='INGRESO').aggregate(Sum('monto'))['monto__sum'] or 0
    egresos_total = totales_contabilidad.filter(tipo='EGRESO').aggregate(Sum('monto'))['monto__sum'] or 0
    
    # Sumamos los pagos de cuotas a los ingresos totales
    total_recaudado_cuotas = PagoCuota.objects.filter(fecha_pago__year=y, fecha_pago__month=m).aggregate(Sum('monto'))['monto__sum'] or 0
    
    ingresos_totales = ingresos_extra + total_recaudado_cuotas

    context = {
        'listado': listado_completo,
        'mes': f"{nombre_mes} {y}",
        'total_ingresos': ingresos_totales,
        'total_egresos': egresos_total,
        'balance_neto': ingresos_totales - egresos_total,
        'actual_month': m,
        'actual_year': y,
    }
    
    return render(request, 'reportes/asistencia_mensual.html', context)