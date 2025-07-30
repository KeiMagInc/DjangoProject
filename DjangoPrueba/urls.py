# DjangoPrueba/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # URL para el formulario de agregar producto
    path('productos/agregar/', views.agregar_producto, name='agregar_producto'),

    # URL para ver los detalles de un producto. El <int:pk> captura el ID del producto.
    path('productos/<int:pk>/', views.detalle_producto, name='detalle_producto'),
]