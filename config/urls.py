"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from usuarios.views import login_view 
from asistencia.views import dashboard 

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 1. El Login ÚNICAMENTE en la raíz
    path('', login_view, name='login'),
    
    # 2. El Dashboard en una ruta clara y distinta
    path('dashboard/', dashboard, name='dashboard'), 
    
    # 3. Aplicaciones con sus nombres de carpeta
    path('usuarios/', include('usuarios.urls')),
    path('asistencia/', include('asistencia.urls')),
    path('pagos/', include('pagos.urls')),
    path('contabilidad/', include('contabilidad.urls')),
    path('reportes/', include('reportes.urls')),
    path('inventario/', include('inventario.urls')),
    
    # 4. IMPORTANTE: Dale un nombre a la ruta de beneficiarios. 
    # Si dejas '', chocará siempre con el login y causará el error de redirección.
    path('beneficiarios/', include('beneficiarios.urls')),
    

]