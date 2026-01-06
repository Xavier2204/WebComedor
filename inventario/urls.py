from django.urls import path
from . import views

urlpatterns = [
    # Panel principal
    path('', views.panel_inventario, name='panel_inventario'),
    
    # Formulario para nuevos productos
    path('nuevo-producto/', views.crear_producto, name='crear_producto'),
    
    # Vista de alertas de stock bajo
    path('alertas/', views.stock_bajo_view, name='alertas_stock'),
    
    # Registro de entradas y salidas (Kardex)
    path('registrar-movimiento/', views.registrar_movimiento, name='registrar_movimiento'),
    path('editar/<int:pk>/', views.editar_producto, name='editar_producto'),
    path('eliminar/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),

]