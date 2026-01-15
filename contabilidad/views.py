from django.shortcuts import render, redirect, get_object_or_404
from .models import Transaccion
from .forms import TransaccionForm
from django.db.models import Sum
from datetime import date
from django.contrib.auth.decorators import login_required, permission_required

@login_required
def finanzas_view(request):
    """
    Cualquier usuario logueado puede ver el balance y las listas.
    La creación de transacciones dentro de esta misma vista se protege con lógica interna.
    """
    if request.method == 'POST':
        # Verificamos permiso antes de procesar el guardado
        if not request.user.has_perm('contabilidad.add_transaccion'):
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied
        
        form = TransaccionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('finanzas')

    transacciones = Transaccion.objects.all().order_by('-fecha')
    ingresos_list = transacciones.filter(tipo='INGRESO')
    egresos_list = transacciones.filter(tipo='EGRESO')

    total_ingresos = ingresos_list.aggregate(Sum('monto'))['monto__sum'] or 0
    total_egresos = egresos_list.aggregate(Sum('monto'))['monto__sum'] or 0
    
    context = {
        'ingresos': ingresos_list,
        'egresos': egresos_list,
        'total_ingresos': total_ingresos,
        'total_egresos': total_egresos,
        'balance': total_ingresos - total_egresos,
        'mes_actual': date.today().strftime('%B %Y'),
        'form': TransaccionForm(),
    }
    return render(request, 'contabilidad/finanzas.html', context)

@login_required
@permission_required('contabilidad.change_transaccion', raise_exception=True)
def editar_transaccion(request, pk):
    transaccion = get_object_or_404(Transaccion, pk=pk)
    if request.method == 'POST':
        form = TransaccionForm(request.POST, instance=transaccion)
        if form.is_valid():
            form.save()
            return redirect('finanzas')
    else:
        form = TransaccionForm(instance=transaccion)
    
    return render(request, 'contabilidad/editar_transaccion.html', {
        'form': form,
        'transaccion': transaccion
    })

@login_required
@permission_required('contabilidad.delete_transaccion', raise_exception=True)
def eliminar_transaccion(request, pk):
    transaccion = get_object_or_404(Transaccion, pk=pk)
    if request.method == 'POST':
        transaccion.delete()
    return redirect('finanzas')

from django.http import HttpResponse

def resetear_ingresos_render(request):
    if request.user.is_superuser:
        # Borramos todos los ingresos para limpiar los datos de prueba
        cantidad = Transaccion.objects.filter(tipo='INGRESO').delete()[0]
        return HttpResponse(f"Se eliminaron {cantidad} registros de ingreso. Ahora el panel debería estar en 0.")
    return HttpResponse("No tienes permiso.")