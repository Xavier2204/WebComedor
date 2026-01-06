from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from beneficiarios.models import Beneficiary
from .models import Attendance
from contabilidad.models import Transaccion 
from datetime import date
from django.db.models import Sum
# Importamos permission_required además de login_required
from django.contrib.auth.decorators import login_required, permission_required

@login_required
def dashboard(request):
    """Vista de visualización: Cualquier usuario logueado puede verla."""
    hoy = date.today()
    total_niños = Beneficiary.objects.count()
    presentes_hoy = Attendance.objects.filter(fecha=hoy).count()
    
    ingresos = Transaccion.objects.filter(tipo='INGRESO').aggregate(Sum('monto'))['monto__sum'] or 0
    egresos = Transaccion.objects.filter(tipo='EGRESO').aggregate(Sum('monto'))['monto__sum'] or 0
    balance = ingresos - egresos

    context = {
        'total_niños': total_niños,
        'presentes_hoy': presentes_hoy,
        'balance': balance,
        'hoy': hoy,
    }
    return render(request, 'index.html', context)

@login_required
def gestion_asistencia(request):
    """Vista de visualización: Cualquier usuario logueado puede ver la lista."""
    hoy = date.today()
    niños = Beneficiary.objects.all().order_by('apellidos')
    asistencias_hoy = Attendance.objects.filter(fecha=hoy).values_list('beneficiary_id', flat=True)

    context = {
        'niños': niños,
        'asistencias_hoy': asistencias_hoy,
        'hoy': hoy,
    }
    return render(request, 'asistencia/gestion.html', context)

@login_required
# Solo permite el acceso si el usuario tiene el permiso de añadir (add) asistencia
@permission_required('asistencia.add_attendance', raise_exception=True)
def marcar_asistencia(request, niño_id):
    niño = get_object_or_404(Beneficiary, id=niño_id)
    hoy = date.today()
    
    Attendance.objects.get_or_create(beneficiary=niño, fecha=hoy)
    messages.success(request, f"Asistencia marcada para {niño.nombre}")

    if request.GET.get('next') == 'gestion':
        return redirect('gestion_asistencia')
    return redirect('dashboard')

@login_required
# Solo permite el acceso si el usuario tiene el permiso de eliminar (delete) asistencia
@permission_required('asistencia.delete_attendance', raise_exception=True)
def desmarcar_asistencia(request, niño_id):
    hoy = date.today()
    Attendance.objects.filter(beneficiary_id=niño_id, fecha=hoy).delete()
    messages.info(request, "Asistencia eliminada correctamente.")
    
    if request.GET.get('next') == 'gestion':
        return redirect('gestion_asistencia')
    return redirect('dashboard')