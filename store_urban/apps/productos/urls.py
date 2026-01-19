from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('genero/<int:genero_id>/', productos_por_genero, name='productos_por_genero'),
    path('producto/variante/<int:variante_id>/', detalle_producto, name='detalle_producto'),
    path('ajax/obtener-variante/', obtener_variante_ajax, name='obtener_variante_ajax'),
    path('subcategoria/<int:subcategoria_id>/', productos_por_subcategoria, name='productos_por_subcategoria'),
   
]
    
