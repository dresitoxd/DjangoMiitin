from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import reverse_lazy

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Cuenta creada con éxito! Ahora puedes iniciar sesión.')
            return redirect('login')  # Redirige al login tras un registro exitoso
        else:
            messages.error(request, 'Hubo un error en el formulario. Verifica los campos.')
    else:
        form = UserCreationForm()

    return render(request, 'users/registro.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    success_url = reverse_lazy('index')
