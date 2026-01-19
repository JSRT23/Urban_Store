from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.http import JsonResponse
from collections import OrderedDict
from django.db.models import Sum
from apps.carrito.models import Carrito
import uuid

# Create your views here.
def layout(request):
    categorias = Categoria.objects.select_related('genero').all()

    total_items = 0
    try:
        carrito = None
        if request.user.is_authenticated:
            carrito = Carrito.objects.filter(usuario=request.user).first()
        else:
            sesion_id = request.session.get("carrito_sesion_id")
            if not sesion_id:
                request.session["carrito_sesion_id"] = str(uuid.uuid4())
                sesion_id = request.session["carrito_sesion_id"]
            carrito = Carrito.objects.filter(sesion_id=sesion_id).first()

        if carrito:
            total_items = carrito.items.aggregate(total=Sum('cantidad'))['total'] or 0
    except:
        pass

    return {
        'categorias': categorias,
        'total_items_carrito': total_items,
    }


def index(request):
    generos = Genero.objects.all()
    ofertas = Ofertas.objects.all()
    coleccion = colecciones.objects.all()
    variantes = ProductoVariante.objects.filter(disponible=True).order_by('-fecha_creacion')
    
    # Agrupar por (producto, color) y conservar el orden por fecha
    agrupadas = OrderedDict()
    for v in variantes:
        clave = (v.producto.id, v.color)
        if clave not in agrupadas:
            agrupadas[clave] = v

    # Tomar solo las primeras 6 combinaciones únicas
    productos_nuevos = list(agrupadas.values())[:8]
    

    context = {
        'generos': generos,
        'productos_nuevos': productos_nuevos,
        'ofertas': ofertas,
        'colecciones': coleccion,
    }
    return render(request, 'index.html', context)


def detalle_producto(request, variante_id):
    variante = get_object_or_404(ProductoVariante, id=variante_id)
    producto = variante.producto
    subcategoria_actual = variante.subcategoria  # Asegúrate que el modelo Variante tiene esto

    # Filtrar variantes del mismo producto, en la misma subcategoría y disponibles
    variantes_filtradas = producto.variantes.filter(
        subcategoria=subcategoria_actual,
        disponible=True
    )

    # Obtener colores únicos de esas variantes filtradas
    colores_disponibles = set(v.color for v in variantes_filtradas)

    # Obtener tallas disponibles solo para el color de la variante actual
    tallas_color_actual = set(
        v.talla for v in variantes_filtradas if v.color == variante.color
    )

    context = {
        'producto': producto,
        'variante': variante,
        'colores': colores_disponibles,
        'tallas': tallas_color_actual,
    }
    return render(request, 'detalle_producto.html', context)

# AJAX para obtener variante por color
def obtener_variante_ajax(request):
    producto_id = request.GET.get('producto_id')
    color_nombre = request.GET.get('color')
    talla_id = request.GET.get('talla_id')

    if not producto_id or not color_nombre:
        return JsonResponse({'error': 'Parámetros inválidos'}, status=400)

    try:
        producto = Producto.objects.get(id=producto_id)
    except Producto.DoesNotExist:
        return JsonResponse({'error': 'Producto no encontrado'}, status=404)

    variantes = ProductoVariante.objects.filter(
        producto=producto,
        color__nombre__iexact=color_nombre,
        disponible=True,
        cantidad__gt=0
    )

    if talla_id:
        variantes = variantes.filter(talla_id=talla_id)

    data = []
    for v in variantes:
        data.append({
            'id': v.id,
            'talla_id': v.talla.id,
            'talla_nombre': v.talla.nombre,
            'precio': v.precio,
            'imagen': v.imagen.url if v.imagen else '',
            'cantidad': v.cantidad,
            'disponible': v.disponible
        })

    return JsonResponse({'variantes': data})

def productos_por_genero(request, genero_id):
    genero = get_object_or_404(Genero, id=genero_id)

    # Solo variantes disponibles y con stock > 0
    productos = ProductoVariante.objects.filter(disponible=True, cantidad__gt=0)

    categoria = genero.categorias.all()
    subcategorias = SubCategoria.objects.all()

    # Agrupar por combinación única para evitar duplicados visuales
    agrupadas = {}
    for v in productos:
        clave = (v.producto.id, v.subcategoria.id, v.color)
        if clave not in agrupadas:
            agrupadas[clave] = v

    producto = list(agrupadas.values())

    context = {
        'genero': genero,
        'categorias': categoria,
        'subcategorias': subcategorias,
        'variante': producto,
    }
    return render(request, 'productos_genero.html', context)

def productos_por_subcategoria(request, subcategoria_id):
    subcategoria = get_object_or_404(SubCategoria, id=subcategoria_id)

    # Solo variantes disponibles y con stock > 0 y que pertenezcan a la subcategoría seleccionada
    productos = ProductoVariante.objects.filter(
        disponible=True,
        cantidad__gt=0,
        subcategoria=subcategoria
    )
    categoria_actual = subcategoria.categoria

    # Obtener el género relacionado
    genero_actual = categoria_actual.genero
    categoria = genero_actual.categorias.all().order_by('genero__nombre')
    generos = Genero.objects.all()

    # Agrupar por combinación única para evitar duplicados visuales
    agrupadas = {}
    for v in productos:
        clave = (v.producto.id, v.subcategoria.id, v.color)
        if clave not in agrupadas:
            agrupadas[clave] = v

    producto = list(agrupadas.values())

    context = {
        'subcategoria': subcategoria,
        'categorias': categoria,
        'genero': generos,
        'variante': producto,
    }
    return render(request, 'productos_subcategoria.html', context)