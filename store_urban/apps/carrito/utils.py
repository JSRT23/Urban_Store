# carrito/utils.py
from .models import Carrito
import uuid

def obtener_carrito(request):
    if request.user.is_authenticated:
        # Si el usuario está autenticado, obtenemos el carrito
        carrito, creado = Carrito.objects.get_or_create(usuario=request.user)
        sub_total = sum(item.subtotal() for item in carrito.items.all())
    else:
        # Si el usuario no está autenticado, buscamos o creamos un carrito con sesion_id
        sesion_id = request.session.get("carrito_sesion_id")
        if not sesion_id:
            # Si no existe un carrito en la sesión, lo creamos
            sesion_id = str(uuid.uuid4())
            request.session["carrito_sesion_id"] = sesion_id
            request.session.save()  # Aseguramos que la sesión se guarde
        carrito, creado = Carrito.objects.get_or_create(sesion_id=sesion_id)
        sub_total = sum(item.subtotal() for item in carrito.items.all())

    return carrito, sub_total