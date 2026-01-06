from django.urls import path
from . import views

urlpatterns = [
    # El 'name' debe ser exactamente este para que el dashboard lo encuentre
    path('mensual/', views.reporte_mensual_integral, name='reporte_asistencia'),
    
    # Ruta para el historial
    path('mensual/<int:year>/<int:month>/', views.reporte_mensual_integral, name='reporte_asistencia_historial'),
]