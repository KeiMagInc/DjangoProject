from django.db import models

# DjangoPrueba/models.py

from django.db import models
from django.urls import reverse

class Producto(models.Model):
    """
    Representa un producto en el catálogo.
    """
    nombre = models.CharField(max_length=200, unique=True, help_text="Nombre del producto")
    precio = models.DecimalField(max_digits=10, decimal_places=2, help_text="Precio del producto")
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-creado_en'] # Ordenar por fecha de creación descendente

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        """
        Devuelve la URL para ver los detalles de esta instancia de Producto.
        Usado por Django después de crear/actualizar un objeto.
        """
        return reverse('detalle_producto', args=[str(self.id)])

