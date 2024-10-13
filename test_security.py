# Test de seguridad
# pytest test_security.py

import pytest
import requests

BASE_URL = 'http://127.0.0.1:5000'  # Cambia esto si tu aplicación corre en otra URL.

# Test de Cross-Site Scripting (XSS)
def test_xss():
    # Intenta inyectar un script en el campo de nombre
    payload = {
        'nombre': '<script>alert("XSS")</script>',
        'peso': '5',
        'tamano': 'mediano',
        'velocidad': 'lenta'
    }
    
    response = requests.post(f"{BASE_URL}/crear", data=payload)
    
    # Verifica que redirija a la página principal sin errores
    assert response.url == f"{BASE_URL}/"

    # Verifica que el script no aparezca en el HTML renderizado (esto requiere una forma de ver la respuesta)
    assert '<script>alert("XSS")</script>' not in response.text

# Asegúrate de que el script no pueda ser ejecutado al renderizar la página
def test_rendered_page():
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    assert '<script>alert("XSS")</script>' not in response.text

# Asegúrate de que tu aplicación tiene algún tipo de protección contra CSRF
# Este test asume que usas un token CSRF en tus formularios.
def test_csrf_protection():
    # Aquí debes agregar un método para obtener el token CSRF de tu formulario
    # Por ejemplo, podrías cargar el formulario y extraer el token
    # Este es un ejemplo básico, modifica según la implementación real
    csrf_token = "some_token"  # Deberías reemplazar esto con el método real para obtener el token.

    payload = {
        'nombre': 'Item de prueba',
        'peso': '5',
        'tamano': 'mediano',
        'velocidad': 'lenta',
        'csrf_token': csrf_token  # Asegúrate de que el token CSRF esté presente.
    }
    
    response = requests.post(f"{BASE_URL}/crear", data=payload)
    assert response.url == f"{BASE_URL}/"

if __name__ == "__main__":
    pytest.main()
