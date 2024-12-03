from django.db import models
from datetime import timedelta
from django.contrib.auth.models import User


class Subasta(models.Model):
    image = models.ImageField(upload_to='subastas_imagen/')
    title = models.CharField(max_length=50)
    description = models.TextField()
    game = models.CharField(max_length=100)
    rarity = models.CharField(max_length=50)
    condition = models.CharField(max_length=50)
    duration = models.PositiveIntegerField()


    def __str__(self):
        return f'{self.title} - {self.game}'

    def delete(self, using=None, keep_parents=False):
        self.image.storage.delete(self.image.name)
        super().delete()

class Carta(models.Model):
    image = models.ImageField(upload_to='cartas_imagen/')
    title = models.CharField(max_length=50)
    description = models.TextField()
    game = models.CharField(max_length=100)
    rarity = models.CharField(max_length=50)
    condition = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=0)  # Precio de la carta

    def __str__(self):
        return f'{self.title} - {self.game}'
    
class Carrito(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Carrito de {self.user.username}"

class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    carta = models.ForeignKey(Carta, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.cantidad} x {self.carta.title}"

    @property
    def total(self):
        return self.carta.price * self.cantidad

class TCG(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
  
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    tcgs = models.ManyToManyField(TCG, blank=True)

    def __str__(self):
        return self.user.username
    
class Inventario(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    carta = models.ForeignKey(Carta, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)  # Cantidad de cartas que posee
    
class Boleta(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Boleta #{self.id} - {self.user.username} - ${self.total}"

class DetalleBoleta(models.Model):
    boleta = models.ForeignKey(Boleta, on_delete=models.CASCADE, related_name='detalles')
    carta = models.ForeignKey(Carta, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.carta.title} x {self.cantidad} - ${self.subtotal}"
