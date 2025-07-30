from django.shortcuts import render

# DjangoPrueba/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Producto
from .forms import ProductoForm


@login_required
def agregar_producto(request):
    """
    Vista para agregar un nuevo producto. Requiere que el usuario esté autenticado.
    - Si la petición es GET, muestra el formulario vacío.
    - Si la petición es POST, procesa los datos del formulario.
    """
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save()
            # Redirige a la página de detalles del producto recién creado
            return redirect(producto.get_absolute_url())
    else:
        # Si es una petición GET, crea una instancia del formulario vacío
        form = ProductoForm()

    # Renderiza la plantilla con el formulario
    return render(request, 'DjangoPrueba/agregar_producto.html', {'form': form})


def detalle_producto(request, pk):
    """
    Muestra los detalles de un producto específico, identificado por su clave primaria (pk).
    """
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'DjangoPrueba/detalle_producto.html', {'producto': producto})
