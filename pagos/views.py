from django.shortcuts import render, redirect, get_object_or_404
from beneficiarios.models import Beneficiary
from .models import PagoCuota
from contabilidad.models import Transaccion
from datetime import date
# Importación de decoradores de seguridad
from django.contrib.auth.decorators import login_required, permission_required

@login_required
def gestion_pagos(request):
    """Cualquier usuario logueado puede ver la lista de pagos."""
    niños = Beneficiary.objects.all()
    return render(request, 'pagos/gestion.html', {'niños': niños})

@login_required
@permission_required('pagos.add_pagocuota', raise_exception=True)
def registrar_pago(request, niño_id):
    """Solo usuarios con permiso de añadir pago pueden ejecutar esto."""
    niño = get_object_or_404(Beneficiary, id=niño_id)
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    mes_actual = meses[date.today().month - 1]
    
    # 1. Crear el registro de pago en la app Pagos
    pago, created = PagoCuota.objects.get_or_create(
        beneficiary=niño,
        mes_correspondiente=mes_actual,
        defaults={'monto': niño.monthly_fee, 'fecha_pago': date.today()}
    )
    
    # 2. Si se creó el pago por primera vez, registrarlo en Contabilidad
    if created:
        # Nota: Asegúrate de que el usuario también tenga permiso en contabilidad si es necesario, 
        # aunque aquí se hace de forma automática por el sistema.
        Transaccion.objects.create(
            tipo='INGRESO',
            categoria='DONACION', 
            monto=niño.monthly_fee,
            descripcion=f"Pago Mensualidad: {niño.apellidos} {niño.nombre} ({mes_actual})",
        )
        
    return redirect('gestion_pagos')

@login_required
@permission_required('pagos.delete_pagocuota', raise_exception=True)
def desmarcar_pago(request, niño_id):
    """Solo usuarios con permiso de borrar pago pueden ejecutar esto."""
    niño = get_object_or_404(Beneficiary, id=niño_id)
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    mes_actual = meses[date.today().month - 1]
    
    # 1. Eliminar el registro en la contabilidad primero
    descripcion_busqueda = f"Pago Mensualidad: {niño.apellidos} {niño.nombre} ({mes_actual})"
    Transaccion.objects.filter(descripcion=descripcion_busqueda, tipo='INGRESO').delete()
    
    # 2. Eliminar el registro de pago
    PagoCuota.objects.filter(beneficiary_id=niño_id, mes_correspondiente=mes_actual).delete()
    
    return redirect('gestion_pagos')