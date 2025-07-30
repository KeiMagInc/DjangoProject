# DjangoPrueba/features/steps/mis_pasos.py

from behave import *
from django.contrib.auth.models import User
from django.urls import reverse
from decimal import Decimal

# Es una buena práctica importar el modelo de forma segura
try:
    from DjangoPrueba.models import Producto
except ImportError:
    Producto = None

# use_step_matcher("re") para expresiones regulares o "parse" para el estilo de llaves
use_step_matcher("parse")


@given('que soy un usuario autenticado')
def step_impl(context):
    """
    Crea un usuario de prueba y lo autentica usando el cliente de pruebas de Django.
    """
    if Producto is None:
        assert False, "El modelo Producto no se pudo importar. ¿Lo has creado en DjangoPrueba/models.py?"

    username = 'testuser'
    password = 'testpassword'
    # Crea el usuario si no existe para evitar errores en ejecuciones repetidas
    if not User.objects.filter(username=username).exists():
        User.objects.create_user(username=username, password=password)

    # Inicia sesión con el cliente de prueba
    context.client.login(username=username, password=password)


@when('voy a la página de "{page_name}"')
def step_impl(context, page_name):
    """
    Navega a una URL específica usando su nombre.
    Esto es más robusto que usar rutas hardcodeadas.
    """
    # Mapea los nombres legibles a los nombres de las rutas de Django
    url_map = {
        "agregar producto": reverse('agregar_producto')
    }
    url = url_map.get(page_name)
    assert url, f"La URL para '{page_name}' no está definida en el mapa de URLs del step."

    # Realiza la petición GET
    context.response = context.client.get(url)
    assert context.response.status_code == 200, f"No se pudo acceder a {url}. Código de estado: {context.response.status_code}"


@when('relleno el nombre con "{nombre}" y el precio con "{precio}"')
def step_impl(context, nombre, precio):
    """
    Almacena los datos del formulario en el contexto para usarlos en el siguiente paso.
    """
    context.form_data = {
        'nombre': nombre,
        'precio': precio
    }


@when('presiono el botón "Guardar"')
def step_impl(context):
    """
    Envía los datos del formulario (almacenados en el contexto) a la página actual.
    Sigue la redirección para obtener la página final.
    """
    assert hasattr(context,
                   'form_data'), "No hay datos de formulario para enviar. ¿Falta el paso 'relleno el nombre con...'?"

    # La URL a la que se envía el POST es la misma a la que se accedió en el GET anterior.
    post_url = context.response.request['PATH_INFO']

    # Realiza la petición POST, 'follow=True' es crucial para seguir la redirección.
    context.response = context.client.post(post_url, data=context.form_data, follow=True)

    # Después de un POST exitoso, se espera una redirección (código 302) y la página final (código 200)
    assert context.response.status_code == 200, "La página no redirigió a una página de éxito (status 200)."


@then('debería ser redirigido a la página de detalles del producto "{nombre_producto}"')
def step_impl(context, nombre_producto):
    """
    Verifica que la redirección nos llevó a la URL correcta del producto recién creado.
    """
    # Recupera el producto de la base de datos para construir la URL esperada
    try:
        producto_creado = Producto.objects.get(nombre=nombre_producto)
    except Producto.DoesNotExist:
        assert False, f"El producto '{nombre_producto}' no fue creado en la base de datos."

    # Construye la URL de detalle esperada
    url_esperada = reverse('detalle_producto', args=[producto_creado.id])

    # context.response.redirect_chain contiene la tupla (URL, status_code) de la redirección
    # La URL final está en context.request
    url_real = context.request.path

    assert url_real == url_esperada, f"Se esperaba ser redirigido a {url_esperada}, pero se fue a {url_real}."


@then('la base de datos debe contener un producto con el nombre "{nombre_producto}"')
def step_impl(context, nombre_producto):
    """
    Verifica que el objeto fue creado y guardado correctamente en la base de datos.
    """
    assert Producto.objects.filter(
        nombre=nombre_producto).exists(), f"El producto '{nombre_producto}' no se encontró en la base de datos."