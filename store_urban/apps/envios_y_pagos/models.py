from django.db import models
from django.conf import settings
from apps.carrito.models import Carrito
from apps.productos.models import ProductoVariante


# --- Tipo de Envío ---
class TipoEnvio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    costo = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.nombre} - ${self.costo}"


# --- Método de Pago ---
class MetodoPago(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre


# --- Dirección de Envío ---
class DireccionEnvio(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True  # ← permite que sea nulo si es usuario anónimo
    ) 
    sesion_id = models.CharField(max_length=100, null=True, blank=True) # Para usuarios anónimos
    nombre = models.CharField(max_length=100)           
    telefono = models.CharField(max_length=15)
    direccion = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=100)
    departamento = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=10)
    tipo_envio = models.ForeignKey(TipoEnvio, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.nombre} - {self.direccion}"


# --- Pedido ---
class Pedido(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True  # ← permite pedidos anónimos
    )
    direccion_envio = models.ForeignKey(DireccionEnvio, on_delete=models.PROTECT)
    metodo_pago = models.ForeignKey(MetodoPago, on_delete=models.PROTECT)
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    pagado = models.BooleanField(default=False)
    estado = models.CharField(
        max_length=50,
        choices=[
            ('pendiente', 'Pendiente'),
            ('procesando', 'Procesando'),
            ('enviado', 'Enviado'),
            ('entregado', 'Entregado'),
        ],
        default='pendiente'
    )

    def __str__(self):
        if self.usuario:
            return f"Pedido #{self.id} - {self.usuario} - {self.estado}"
        return f"Pedido #{self.id} - Anónimo - {self.estado}"


# --- Detalle de Pedido ---
class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    variante = models.ForeignKey(ProductoVariante, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        cliente = self.pedido.usuario.username if self.pedido.usuario else "Anónimo"
        return f"{self.variante} x{self.cantidad} (Pedido #{self.pedido.id}) - Cliente: {cliente}"

