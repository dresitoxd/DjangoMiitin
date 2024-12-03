from django import forms
from .models import *


class SubastaForm(forms.ModelForm):
    GAME_CHOICES = [
        ('Mitos y Leyendas', 'Mitos y Leyendas'),
        ('Yu Gi Oh!', 'Yu Gi Oh!'),
        ('Pokemon TCG', 'Pokemon TCG'),
    ]

    DURATION_CHOICES = [(i, f"{i:02d} horas") for i in range(1, 25)]

    RAREZA_CHOICES = [
        ('Normal', 'Normal'),
        ('Real', 'Real'),
        ('Ultra real', 'Ultra real'),
        ('Mega Real', 'Mega Real'),
        ('Legendaria', 'Legendaria'),
    ]

    CONDICION_CHOICES = [
        ('Nueva', 'Nueva'),
        ('Seminueva', 'Seminueva'),
        ('Usada', 'Usada'),
    ]

    game = forms.ChoiceField(choices=GAME_CHOICES, label="Juego")
    duration = forms.ChoiceField(choices=DURATION_CHOICES, label="Duración")
    rareza = forms.ChoiceField(choices=RAREZA_CHOICES, label="Rareza")
    condicion = forms.ChoiceField(choices=CONDICION_CHOICES, label="Condición")

    class Meta:
        model = Subasta
        fields = ['image', 'title', 'description', 'game', 'rareza', 'condicion', 'duration']
        labels = {
            'image': 'Imagen',
            'title': 'Título',
            'description': 'Descripción',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class CartaForm(forms.ModelForm):
    GAME_CHOICES = [
        ('Mitos y Leyendas', 'Mitos y Leyendas'),
        ('Yu Gi Oh!', 'Yu Gi Oh!'),
        ('Pokemon TCG', 'Pokemon TCG'),
    ]

    RAREZA_CHOICES = [
        ('Normal', 'Normal'),
        ('Real', 'Real'),
        ('Ultra real', 'Ultra real'),
        ('Mega Real', 'Mega Real'),
        ('Legendaria', 'Legendaria'),
    ]

    CONDICION_CHOICES = [
        ('Nueva', 'Nueva'),
        ('Seminueva', 'Seminueva'),
        ('Usada', 'Usada'),
    ]

    game = forms.ChoiceField(choices=GAME_CHOICES, label="Juego")
    rareza = forms.ChoiceField(choices=RAREZA_CHOICES, label="Rareza")
    condicion = forms.ChoiceField(choices=CONDICION_CHOICES, label="Condición")

    class Meta:
        model = Carta
        fields = ['image', 'title', 'description', 'game', 'rareza', 'condicion', 'price']
        labels = {
            'image': 'Imagen',
            'title': 'Título',
            'description': 'Descripción',
            'price': 'Precio',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'price': forms.TextInput(attrs={
                'class': 'price-input',  # Clase personalizada
                'placeholder': 'Ingrese el precio en CLP',  # Placeholder opcional
            }),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['description', 'profile_picture', 'tcgs']
        widgets = {
            'tcgs': forms.CheckboxSelectMultiple,  # Permite seleccionar varios TCGs
        }