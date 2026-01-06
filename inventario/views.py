from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import models
from .models import Producto
# IMPORTANTE: Importar el formulario
from .forms import ProductoForm, MovimientoForm 

@login_required
def panel_inventario(request):
    productos = Producto.objects.all()
    alertas_count = Producto.objects.filter(
        cantidad_actual__lte=models.F('cantidad_minima')
    ).count()
    
    return render(request, 'inventario/panel.html', {
        'productos': productos,
        'total_productos': productos.count(),
        'alertas_count': alertas_count,
    })

@login_required
def crear_producto(request):
    if request.method == 'POST':
        # 1. Llenamos el formulario con los datos que envió el usuario
        form = ProductoForm(request.POST)
        # 2. Validamos si los datos son correctos
        if form.is_valid():
            form.save() # 3. Guardamos en la base de datos
            return redirect('panel_inventario') # 4. Volvemos al panel
    else:
        # Si es la primera vez que entra, el formulario está vacío
        form = ProductoForm()
    
    # 5. Pasamos el 'form' al HTML para que se vea
    return render(request, 'inventario/crear_producto.html', {'form': form})

@login_required
def registrar_movimiento(request):
    if request.method == 'POST':
        form = MovimientoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('panel_inventario')
    else:
        form = MovimientoForm()
    return render(request, 'inventario/registrar_movimiento.html', {'form': form})

def stock_bajo_view(request):
    alertas = Producto.objects.filter(cantidad_actual__lte=models.F('cantidad_minima'))
    return render(request, 'inventario/stock_bajo.html', {'alertas': alertas})

def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('panel_inventario')
    else:
        form = ProductoForm(instance=producto)
    
    return render(request, 'inventario/crear_producto.html', {
        'form': form,
        'producto': producto,  # Importante para el Modal de borrar
        'editando': True       # Importante para que aparezca el botón rojo
    })

def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
    return redirect('panel_inventario')