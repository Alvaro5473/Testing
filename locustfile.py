"""
Test de rendimiento
locust -f locustfile.py
coverage run locustfile.py
"""

from locust import HttpUser, task, between

class ItemUser(HttpUser):
    """Test de rendimiento"""
    host = "http://127.0.0.1:5000"  # Especifica el host de tu aplicación Flask
    wait_time = between(1, 3)  # Tiempo de espera entre las solicitudes, en segundos

    @task
    def crear_item(self):
        """Crear item"""
        payload = {
            'nombre': 'Item de prueba',
            'peso': '5',
            'tamano': 'mediano',
            'velocidad': 'lenta'
        }
        self.client.post("/crear", data=payload)

    @task
    def obtener_items(self):
        """Obtener items"""
        self.client.get("/")

if __name__ == "__main__":
    import os
    os.system("locust -f locustfile.py")
