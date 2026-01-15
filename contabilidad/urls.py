from django.urls import path
from . import views

urlpatterns = [
    path('', views.finanzas_view, name='finanzas'),
    path('editar/<int:pk>/', views.editar_transaccion, name='editar_transaccion'),
    path('eliminar/<int:pk>/', views.eliminar_transaccion, name='eliminar_transaccion'),
    path('reset-datos-secreto/', views.resetear_ingresos_render),]