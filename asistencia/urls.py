from django.urls import path
from .views import marcar_asistencia
from . import views

urlpatterns = [
    path('gestion/', views.gestion_asistencia, name='gestion_asistencia'),
    path('marcar/<int:niño_id>/', marcar_asistencia, name='marcar_asistencia'),
    path('desmarcar/<int:niño_id>/', views.desmarcar_asistencia, name='desmarcar_asistencia'),
]