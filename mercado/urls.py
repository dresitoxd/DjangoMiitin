from django.urls import path
from . import views
from django.conf import settings
from django.contrib.staticfiles.urls import static
urlpatterns = [
    path('', views.index, name='index'),
    path('subastas/', views.listar_subastas, name='subasta'),
    path('crear-subasta/', views.crear_subasta, name='crear_subasta'),
    path('crear-carta/', views.crear_carta, name='crear_carta'),
    path('subasta/<int:subasta_id>/', views.subasta_detalle, name='subasta_detalle'),
    path('tienda/', views.tienda, name='tienda'),
    path('añadir-al-carrito/<int:carta_id>/', views.añadir_al_carrito, name='añadir_al_carrito'),
    path('carrito/', views.carrito, name='carrito'),
    path('carritoDash/', views.carrito_dashboard, name='carrito_dashboard'),
    path('boleta/', views.boleta_pago, name='boleta'),
    path('Openai/', views.chatbot, name='chatbot_page'),
    path('respuesta/', views.respuesta),
    path('perfil/', views.perfil, name='perfil'),
    path('editar-perfil/', views.editar_perfil, name='editar_perfil'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

