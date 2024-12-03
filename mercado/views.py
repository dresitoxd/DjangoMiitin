from openai import OpenAI
import json
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .forms import *
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from datetime import datetime
from django.utils import timezone
from urllib.parse import parse_qs

def index(request):
    return render(request, 'tienda/index.html')

def listar_subastas(request):
    subastas = Subasta.objects.all()
    return render(request, 'tienda/subastas.html', {'subastas': subastas})


def crear_subasta(request):
    if request.method == 'POST':
        form = SubastaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('subasta')
    else:
        form = SubastaForm()

    return render(request, 'tienda/crear_subasta.html', {'form': form})

def crear_carta(request):
    if request.method == 'POST':
        form = CartaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('tienda')
    else:
        form = CartaForm()

    return render(request, 'tienda/crear_carta.html', {'form': form})

@login_required
def perfil(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        perfil_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if perfil_form.is_valid():
            perfil_form.save()
            return redirect('perfil')  # Redirige al perfil tras guardar
    else:
        perfil_form = UserProfileForm(instance=user_profile)

    return render(request, 'tienda/perfil.html', {
        'perfil_form': perfil_form,
        'user_profile': user_profile,
    })

@login_required
def editar_perfil(request):
    user_profile = request.user.userprofile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('perfil')  # Redirige al perfil después de guardar
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'tienda/editar_perfil.html', {'form': form})

def subasta_detalle(request, subasta_id):
    subasta = get_object_or_404(Subasta, id=subasta_id)
    pujas = subasta.pujas.all()
    return render(request, 'tienda/subastas.html', {'subasta': subasta, 'pujas': pujas})


def tienda(request):
    cartas = Carta.objects.all()  # Asegúrate de que estás pasando todas las cartas
    return render(request, 'tienda/tienda.html', {'cartas': cartas})

@login_required
def añadir_al_carrito(request, carta_id):
    carta = get_object_or_404(Carta, id=carta_id)
    cantidad = int(request.POST.get('cantidad', 1))  # Obtén la cantidad del formulario, valor predeterminado es 1

    carrito, created = Carrito.objects.get_or_create(user=request.user)

    # Verifica si el ítem ya está en el carrito
    item, created = ItemCarrito.objects.get_or_create(carrito=carrito, carta=carta, defaults={'cantidad': cantidad})

    if not created:
        # Si ya existe, actualiza la cantidad
        item.cantidad += cantidad
        item.save()

    return redirect('tienda')  # Cambia 'tienda' por el nombre de tu vista o URL de la tienda

@login_required
def carrito(request):
    carrito = Carrito.objects.get(user=request.user)
    items = ItemCarrito.objects.filter(carrito=carrito)

    return render(request, 'tienda/carrito_dashboard.html', {'carrito': carrito, 'items': items})

def carrito_dashboard(request):
    try:
        carrito = Carrito.objects.get(user=request.user)
        items = ItemCarrito.objects.filter(carrito=carrito)
        total_carrito = sum(item.total for item in items)

        # Debugging
        for item in items:
            print(f"{item.carta.title} x {item.cantidad} = ${item.total}")
        print(f"Total del carrito: ${total_carrito}")

    except Carrito.DoesNotExist:
        carrito = None
        items = []
        total_carrito = 0

    return render(request, 'tienda/carrito_dashboard.html', {
        'carrito': carrito,
        'items': items,
        'total_carrito': total_carrito
    })


def boleta_pago(request):
    try:
        carrito = Carrito.objects.get(user=request.user)
        items = ItemCarrito.objects.filter(carrito=carrito)

        if not items:
            return render(request, 'tienda/boleta_vacia.html', {'mensaje': 'El carrito está vacío.'})

        total_carrito = sum(item.total for item in items)
        fecha = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

        # Guardar boleta y detalles dentro de una transacción
        with transaction.atomic():
            # Crear boleta
            boleta = Boleta.objects.create(user=request.user, total=total_carrito)

            # Crear detalles de la boleta
            for item in items:
                DetalleBoleta.objects.create(
                    boleta=boleta,
                    carta=item.carta,
                    cantidad=item.cantidad,
                    subtotal=item.total
                )

            # Limpiar el carrito
            items.delete()

        return render(request, 'tienda/boleta.html', {
            'user': request.user,
            'items': boleta.detalles.all(),
            'total_carrito': total_carrito,
            'fecha': fecha
        })

    except Carrito.DoesNotExist:
        return render(request, 'tienda/boleta_vacia.html', {'mensaje': 'No se encontró el carrito.'})


def lista_intercambios(request):
    
    return render(request, 'tienda/intercambios.html', {})

# Vista para mostrar la página del chatbot
def chatbot_page(request):
    return render(request, 'tienda/chatbot.html')



def chatbot(request):
    return render(request, 'tienda/chatbot.html')

client= OpenAI()

def generar_respuesta (question):
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": question}],
        stream = True
    )

    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            yield(chunk.choices[0].delta.content)
@csrf_exempt
def respuesta(request):
    data = json.loads(request.body)
    message = data["message"]
    response = StreamingHttpResponse(generar_respuesta(message), status=200, content_type="text/plain")
    return response

