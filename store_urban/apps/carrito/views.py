from django.shortcuts import render, get_object_or_404, redirect
from .utils import obtener_carrito  # Import the function from the appropriate module
from apps.productos.models import ProductoVariante  # Import the ProductoVariante model
from .models import ItemCarrito, Carrito  # Import the ItemCarrito model
from django.contrib import messages

# Create your views here.
def ver_carrito(request):
    carrito, sub_total = obtener_carrito(request)
    items = carrito.items.select_related('variante', 'variante__producto')

    # Calcular el subtotal de los productos
    subtotal = sum(item.subtotal() for item in items)
    
    # Determinar el costo de envío
    envio = 0
    envio_gratis = False
    falta_envio_gratis = 200000 - subtotal

    if subtotal >= 200000:
        envio_gratis = True
    else:
        envio = 15000
        
    total = subtotal + envio
    
    return render(request, 'carrito.html', {
        'carrito': carrito,
        'items': items,
        'total': total,
        'envio': envio,
        'envio_gratis': envio_gratis,
        'falta_envio_gratis': falta_envio_gratis,
        'subtotal': subtotal,
    })
    
def agregar_al_carrito(request):
    if request.method == 'POST':
        variante_id = request.POST.get('variante_id')
        cantidad = int(request.POST.get('cantidad', 1))

        # Obtén la variante del producto
        variante = get_object_or_404(ProductoVariante, id=variante_id)

        # Obtén el carrito del usuario
        carrito, _ = obtener_carrito(request)

        # Crear o actualizar el item en el carrito
        item, creado = ItemCarrito.objects.get_or_create(
            carrito=carrito,
            variante=variante,
            defaults={'cantidad': cantidad}
        )

        if not creado:
            # Verifica si hay suficiente stock para aumentar la cantidad
            if item.cantidad + cantidad <= variante.cantidad:
                item.cantidad += cantidad
                item.save()
                messages.success(request, 'Se agregó el producto a tu carrito')
            else:
                messages.error(request, f'No puedes agregar más de {variante.cantidad} unidades')
        else:
            messages.success(request, 'Se agregó el producto a tu carrito')

    return redirect('detalle_producto', variante_id=variante_id)  # Cambia a la vista de detalle del producto
    
def actualizar_item(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id)
    if request.method == 'POST':
        nueva_cantidad = int(request.POST.get('cantidad', 1))
        
        # Verifica que la nueva cantidad no exceda el stock
        if nueva_cantidad <= item.variante.cantidad:
            item.cantidad = nueva_cantidad
            item.save()
            messages.success(request, 'El carrito se actualizó correctamente')
        else:
            messages.error(request, f'No puedes agregar más de {item.variante.cantidad} unidades')
    
    return redirect('ver_carrito')

def eliminar_item(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id)
    item.delete()
    messages.success(request, 'Producto eliminado del carrito')
    return redirect('ver_carrito')

def vaciar_carrito(request):
    carrito = None

    if request.user.is_authenticated:
        carrito = Carrito.objects.filter(usuario=request.user).first()
    else:
        sesion_id = request.session.session_key
        if not sesion_id:
            request.session.create()
            sesion_id = request.session.session_key
        carrito = Carrito.objects.filter(sesion_id=sesion_id).first()

    if carrito:
        carrito.items.all().delete()
        messages.success(request, 'Tu carrito ha sido vaciado')
    else:
        messages.info(request, 'No tienes un carrito para vaciar.')

    return redirect('ver_carrito')