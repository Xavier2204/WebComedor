from django.urls import path
from . import views

urlpatterns = [
    path('gestion/', views.gestion_pagos, name='gestion_pagos'),
    path('registrar/<int:niño_id>/', views.registrar_pago, name='registrar_pago'),
    path('desmarcar/<int:niño_id>/', views.desmarcar_pago, name='desmarcar_pago'),
]