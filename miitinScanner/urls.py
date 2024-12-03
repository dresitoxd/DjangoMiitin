from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', include('usuarios.urls')),  # Redirige la ruta '/login' a la app 'usuarios'
    path('registro/', include('usuarios.urls')),  # Redirige la ruta '/registro' a la app 'usuarios'
    path('', include('mercado.urls')),  # La app 'mercado' está disponible en la raíz
]
