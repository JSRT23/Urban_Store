from django.urls import path
from .views import *

urlpatterns = [
    path('direccion/', direccion_envio, name='direccion_envio'),
    path('checkout/', checkout, name='checkout'),
    path('confirmar-compra/', confirmar_compra, name='confirmar_compra'),
    path('direccion/editar/<int:pk>/', editar_direccion, name='editar_direccion'),
]