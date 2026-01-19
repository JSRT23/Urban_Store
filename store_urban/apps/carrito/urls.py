from django.urls import path
from .views import *

urlpatterns = [
    path('carrito/', ver_carrito, name='ver_carrito'),
    path('agregar/', agregar_al_carrito, name='agregar_al_carrito'),
    path('actualizar/<int:item_id>/', actualizar_item, name='actualizar_item'),
    path('eliminar/<int:item_id>/', eliminar_item, name='eliminar_item'),
    path('vaciar/', vaciar_carrito, name='vaciar_carrito'),
]