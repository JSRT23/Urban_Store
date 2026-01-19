from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from apps.carrito.models import *
from apps.carrito.utils import obtener_carrito
from django.contrib import messages
from datetime import datetime
# Create your views here.

def direccion_envio(request):
    carrito = obtener_carrito(request)

    if request.method == 'POST':
        # Obtener datos del formulario
        nombre = request.POST.get('nombre')
        telefono = request.POST.get('telefono')
        direccion = request.POST.get('direccion')
        ciudad = request.POST.get('ciudad')
        departamento = request.POST.get('departamento')
        codigo_postal = request.POST.get('codigo_postal')
        tipo_envio_id = request.POST.get('tipo_envio')

        tipo_envio = get_object_or_404(TipoEnvio, id=tipo_envio_id)

        if request.user.is_authenticated:
            direccion_envio = DireccionEnvio.objects.create(
                usuario=request.user,
                nombre=nombre,
                telefono=telefono,
                direccion=direccion,
                ciudad=ciudad,
                departamento=departamento,
                codigo_postal=codigo_postal,
                tipo_envio=tipo_envio
            )
        else:
            if not request.session.session_key:
                request.session.create()
            sesion_id = request.session.session_key

            direccion_envio = DireccionEnvio.objects.create(
                sesion_id=sesion_id,
                nombre=nombre,
                telefono=telefono,
                direccion=direccion,
                ciudad=ciudad,
                departamento=departamento,
                codigo_postal=codigo_postal,
                tipo_envio=tipo_envio
            )

        # Guardamos en sesión para usarla en el checkout
        request.session['direccion_envio_id'] = direccion_envio.id

        return redirect('checkout')

    tipos_envio = TipoEnvio.objects.all()
    return render(request, 'direccion_envio.html', {'tipos_envio': tipos_envio})


#Editar direccion de envio
def editar_direccion(request, pk):
    direccion = DireccionEnvio.objects.get(usuario=request.user)
    tipos_envio = TipoEnvio.objects.all()  # Para el select
     
    if request.method == 'POST':
        direccion.nombre_completo = request.POST.get('nombre')
        direccion.direccion = request.POST.get('direccion')
        direccion.ciudad = request.POST.get('ciudad')
        direccion.departamento = request.POST.get('departamento')
        direccion.codigo_postal = request.POST.get('codigo_postal')
        direccion.pais = request.POST.get('pais')
        direccion.telefono = request.POST.get('telefono')
        direccion.tipo_envio_id = request.POST.get('tipo_envio')
        
        direccion.save()  # No le pases nada aquí
        return redirect('checkout')
    return render(request, 'editar_envio.html', {
        'direccion': direccion,
        'tipos_envio': tipos_envio
    })


#Checkout
def checkout(request):
    carrito, sub_total = obtener_carrito(request)

    # Métodos de pago disponibles
    metodos_pago = MetodoPago.objects.all()

    # Obtener dirección de envío según tipo de usuario
    direccion_envio = None

    if request.user.is_authenticated:
        direccion_envio = DireccionEnvio.objects.filter(usuario=request.user).last()
    else:
        direccion_id = request.session.get('direccion_envio_id')
        if direccion_id:
            direccion_envio = get_object_or_404(DireccionEnvio, id=direccion_id)

    # Fecha actual
    fecha = datetime.now()

    # Cálculo de costos de envío
    costo_envio = direccion_envio.tipo_envio.costo if direccion_envio and direccion_envio.tipo_envio else 0
    if sub_total >= 200000:
        costo_envio = 0  # Envío gratis para compras mayores a 200000

    total = sub_total + costo_envio

    contexto = {
        'carrito': carrito,
        'items': carrito.items.select_related('variante'),
        'metodos_pago': metodos_pago,
        'direccion_envio': direccion_envio,
        'sub_total': sub_total,
        'costo_envio': costo_envio,
        'total': total,
        'fecha': fecha,
    }

    return render(request, 'checkout.html', contexto)

#Confirmar la compra
def confirmar_compra(request):
    # Obtener el carrito actual con la función reutilizable
    carrito, _ = obtener_carrito(request)

    if not carrito or not carrito.items.exists():
        messages.error(request, 'No hay productos en el carrito para procesar el pedido.')
        return redirect('checkout')

    # Obtener los datos del formulario
    direccion_id = request.POST.get('direccion_id')
    metodo_pago_id = request.POST.get('metodo_pago_id')

    # Validar dirección
    if not direccion_id:
        messages.error(request, 'Por favor selecciona una dirección de envío.')
        return redirect('checkout')

    # Validar método de pago
    if not metodo_pago_id:
        messages.error(request, 'Por favor selecciona un método de pago.')
        return redirect('checkout')

    # Obtener objetos relacionados
    direccion = get_object_or_404(DireccionEnvio, id=direccion_id)
    metodo_pago = get_object_or_404(MetodoPago, id=metodo_pago_id)

    # Calcular total
    total = sum(item.subtotal() for item in carrito.items.all())

    # Crear pedido
    pedido = Pedido.objects.create(
        usuario=request.user if request.user.is_authenticated else None,
        direccion_envio=direccion,
        metodo_pago=metodo_pago,
        carrito=carrito,
        fecha_pedido=datetime.now(),
        total=total,
        pagado=True,
        estado='procesando',
    )

    # Crear detalles del pedido y actualizar stock
    for item in carrito.items.all():
        DetallePedido.objects.create(
            pedido=pedido,
            variante=item.variante,
            cantidad=item.cantidad,
            precio_unitario=item.variante.precio
        )
        item.variante.cantidad -= item.cantidad
        if item.variante.cantidad <= 0:
            item.variante.cantidad = 0
            item.variante.disponible = False
        item.variante.save()

    # Vaciar el carrito (no eliminarlo)
    carrito.items.all().delete()

    return render(request, 'factura.html', {'pedido': pedido})

