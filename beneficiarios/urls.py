from django.urls import path
from . import views

urlpatterns = [
    # Panel Principal
    path('', views.dashboard, name='dashboard'),
    
    # Gestión de Beneficiarios
    path('nuevo/', views.crear_beneficiario, name='crear_beneficiario'),
    path('<int:pk>/', views.perfil_beneficiario, name='perfil_beneficiario'),
    path('<int:pk>/editar/', views.editar_beneficiario, name='editar_beneficiario'),
    path('<int:pk>/eliminar/', views.eliminar_beneficiario, name='eliminar_beneficiario'),
    
    # Gestión de Representantes
    path('representante/nuevo/', views.crear_representante, name='crear_representante'),
]