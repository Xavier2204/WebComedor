from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Sum, F
from datetime import date

# Importación de modelos de la propia app
from .models import Beneficiary, Representative, Enrollment
from .forms import BeneficiaryForm, RepresentativeForm, EnrollmentForm 

# Importación de modelos de otras apps
from asistencia.models import Attendance
from contabilidad.models import Transaccion
from pagos.models import PagoCuota
from inventario.models import Producto  # <--- Importante para el botón de inventario

@login_required
def dashboard(request):
    """Panel principal con indicadores de todas las apps, incluyendo Inventario."""
    hoy = date.today()
    
    # 1. Listado de niños (Solo activos para el control diario)
    niños_listado = Beneficiary.objects.filter(active=True)
    
    # Marcamos dinámicamente quién asistió hoy para el HTML
    for niño in niños_listado:
        niño.asistio_hoy = Attendance.objects.filter(
            beneficiary=niño, 
            fecha=hoy, 
            llego_puntual=True
        ).exists()

    # 2. Cálculos de Asistencia
    presentes_hoy = Attendance.objects.filter(fecha=hoy, llego_puntual=True).count()

    # 3. Finanzas (Ingresos de Cuotas + Ingresos Extra - Egresos)
    ingresos_cuotas = PagoCuota.objects.aggregate(total=Sum('monto'))['total'] or 0
    ingresos_extra = Transaccion.objects.filter(tipo='INGRESO').aggregate(total=Sum('monto'))['total'] or 0
    total_ingresos = ingresos_cuotas + ingresos_extra
    
    total_egresos = Transaccion.objects.filter(tipo='EGRESO').aggregate(total=Sum('monto'))['total'] or 0
    balance = total_ingresos - total_egresos

    # 4. Pagos Pendientes (Lógica basada en tu modelo Beneficiary)
    pagos_pendientes = sum(1 for n in niños_listado if not n.tiene_pago_mes_actual())

    # 5. Cálculo de Inventario (Productos con stock bajo o agotado)
    # Comparamos cantidad_actual con cantidad_minima
    total_alertas = Producto.objects.filter(
        cantidad_actual__lte=F('cantidad_minima')
    ).count()

    context = {
        'niños_listado': niños_listado,
        'presentes': presentes_hoy,
        'ingresos': total_ingresos,
        'egresos': total_egresos,
        'balance': balance,
        'hoy': hoy,
        'pendientes_conteo': pagos_pendientes,
        'total_alertas': total_alertas, # <--- Enviado al index.html para la card de inventario
    }
    return render(request, 'index.html', context)

@login_required
@permission_required('beneficiarios.add_representative', raise_exception=True)
def crear_representante(request):
    if request.method == 'POST':
        form = RepresentativeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crear_beneficiario')
    else:
        form = RepresentativeForm()
    return render(request, 'beneficiarios/crear_representante.html', {'form': form})

@login_required
@permission_required('beneficiarios.add_beneficiary', raise_exception=True)
def crear_beneficiario(request):
    if request.method == 'POST':
        form = BeneficiaryForm(request.POST)
        enroll_form = EnrollmentForm(request.POST) 
        if form.is_valid() and enroll_form.is_valid():
            niño = form.save()
            inscripcion = enroll_form.save(commit=False)
            inscripcion.beneficiary = niño
            inscripcion.save()
            return redirect('dashboard')
    else:
        form = BeneficiaryForm()
        enroll_form = EnrollmentForm()
    return render(request, 'beneficiarios/crear_beneficiario.html', {
        'form': form, 
        'enroll_form': enroll_form
    })

@login_required
def perfil_beneficiario(request, pk):
    niño = get_object_or_404(Beneficiary, pk=pk)
    inscripcion = Enrollment.objects.filter(beneficiary=niño).first()
    context = {'niño': niño, 'inscripcion': inscripcion}
    return render(request, 'beneficiarios/perfil.html', context)

@login_required
@permission_required('beneficiarios.change_beneficiary', raise_exception=True)
def editar_beneficiario(request, pk):
    niño = get_object_or_404(Beneficiary, pk=pk)
    inscripcion = Enrollment.objects.filter(beneficiary=niño).first()
    if request.method == 'POST':
        form = BeneficiaryForm(request.POST, instance=niño)
        enroll_form = EnrollmentForm(request.POST, instance=inscripcion)
        if form.is_valid() and enroll_form.is_valid():
            form.save()
            nueva_inscripcion = enroll_form.save(commit=False)
            nueva_inscripcion.beneficiary = niño
            nueva_inscripcion.save()
            return redirect('perfil_beneficiario', pk=niño.pk)
    else:
        form = BeneficiaryForm(instance=niño)
        enroll_form = EnrollmentForm(instance=inscripcion)
    return render(request, 'beneficiarios/crear_beneficiario.html', {
        'form': form, 
        'enroll_form': enroll_form,
        'editando': True
    })

@login_required
@permission_required('beneficiarios.delete_beneficiary', raise_exception=True)
def eliminar_beneficiario(request, pk):
    niño = get_object_or_404(Beneficiary, pk=pk)
    if request.method == 'POST':
        niño.delete()
        return redirect('dashboard')
    return render(request, 'beneficiarios/confirmar_eliminar.html', {'niño': niño})