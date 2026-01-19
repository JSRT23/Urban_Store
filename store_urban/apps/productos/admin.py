from django.contrib import admin
from .models import Genero, Categoria, SubCategoria, Color, Talla, Producto, ProductoVariante , Ofertas, colecciones
# Register your models here.
admin.site.register(Genero)
admin.site.register(Categoria)
admin.site.register(SubCategoria)
admin.site.register(Color)
admin.site.register(Talla)
admin.site.register(Producto)
admin.site.register(ProductoVariante)
admin.site.register(Ofertas)
admin.site.register(colecciones)