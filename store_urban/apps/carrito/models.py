from django.db import models
from django.conf import settings
from apps.productos.models import ProductoVariante
# Create your models here.
class Carrito(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        null=True, blank=True
    )
    # Para usuarios no autenticados: se genera un ID único para la sesión
    sesion_id = models.CharField(max_length=100, null=True, blank=True)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.usuario:
            return f"Carrito de {self.usuario}"
        return f"Carrito Anónimo - {self.sesion_id}"


class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, related_name='items', on_delete=models.CASCADE)
    variante = models.ForeignKey(ProductoVariante, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.variante} x{self.cantidad}"
    
    def subtotal(self):
        return self.variante.precio * self.cantidad