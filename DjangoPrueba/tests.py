# DjangoPrueba/tests.py
from django.test import TestCase
from hypothesis import given, strategies as st
from .models import Producto # Asumiendo el modelo Producto

class ProductModelTests(TestCase):

    @given(
        nombre=st.text(min_size=1, max_size=100),
        precio=st.decimals(min_value=0.01, max_value=10000.00, places=2)
    )
    def test_property_crear_producto_siempre_es_valido(self, nombre, precio):
        """
        Propiedad: No importa el nombre o precio (dentro de lo razonable),
        el producto creado debe mantener sus valores.
        """
        # Hypothesis generará cientos de combinaciones de nombre y precio
        producto = Producto.objects.create(nombre=nombre, precio=precio)
        self.assertEqual(producto.nombre, nombre)
        self.assertEqual(producto.precio, precio)