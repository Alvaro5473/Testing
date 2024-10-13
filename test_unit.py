# Test unitario
# python test_unit.py

import unittest
import json
from app import app, crear_tabla, conectar_db

class APITestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Crea la tabla antes de las pruebas
        crear_tabla()

    def setUp(self):
        # Configura la aplicación para las pruebas
        self.app = app.test_client()
        self.app.testing = True

        # Borra la base de datos para cada prueba
        self._limpiar_db()

    def _limpiar_db(self):
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM items')
        conn.commit()
        conn.close()

    def test_crear_item(self):
        response = self.app.post('/crear', 
                                 data={
                                     "nombre": "Item 1", 
                                     "peso": "10kg", 
                                     "tamano": "30cm", 
                                     "velocidad": "100km/h"
                                 })
        self.assertEqual(response.status_code, 302)  # Redirección
        # Verificamos que el item fue creado
        response = self.app.get('/')
        self.assertIn(b'Item 1', response.data)

    def test_obtener_items(self):
        self.app.post('/crear', 
                      data={
                          "nombre": "Item 1", 
                          "peso": "10kg", 
                          "tamano": "30cm", 
                          "velocidad": "100km/h"
                      })
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Item 1', response.data)

    def test_obtener_item(self):
        self.app.post('/crear', 
                      data={
                          "nombre": "Item 2", 
                          "peso": "20kg", 
                          "tamano": "40cm", 
                          "velocidad": "200km/h"
                      })
        # Obtener el ID del item recién creado
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Item 2', response.data)

        # Buscamos el ID basado en el nombre en la lista
        # En lugar de asumir que el ID es 1, lo buscamos en la respuesta
        item_id = self.obtener_id_por_nombre('Item 2')
        
        response = self.app.get(f'/actualizar/{item_id}')  # Usar el ID correcto
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Item 2', response.data)

    def obtener_id_por_nombre(self, nombre):
        # Función auxiliar para obtener el ID de un item por su nombre
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM items WHERE nombre = ?', (nombre,))
        item = cursor.fetchone()
        conn.close()
        return item[0] if item else None

    def test_actualizar_item(self):
        self.app.post('/crear', 
                      data={
                          "nombre": "Item 3", 
                          "peso": "30kg", 
                          "tamano": "50cm", 
                          "velocidad": "300km/h"
                      })
        item_id = self.obtener_id_por_nombre('Item 3')  # Obtener el ID del item creado
        response = self.app.post(f'/actualizar/{item_id}', 
                                 data={
                                     "nombre": "Item 3 actualizado", 
                                     "peso": "35kg", 
                                     "tamano": "55cm", 
                                     "velocidad": "350km/h"
                                 })
        self.assertEqual(response.status_code, 302)  # Redirección después de actualizar
        # Verificamos que el item fue actualizado
        response = self.app.get('/')
        self.assertIn(b'Item 3 actualizado', response.data)

    def test_eliminar_item(self):
        self.app.post('/crear', 
                      data={
                          "nombre": "Item 4", 
                          "peso": "40kg", 
                          "tamano": "60cm", 
                          "velocidad": "400km/h"
                      })
        item_id = self.obtener_id_por_nombre('Item 4')  # Obtener el ID del item creado
        response = self.app.post(f'/eliminar/{item_id}')  # Eliminar el item creado
        self.assertEqual(response.status_code, 302)  # Redirección después de eliminar

        # Verificamos que el item ha sido eliminado
        response = self.app.get('/')
        self.assertNotIn(b'Item 4', response.data)

if __name__ == '__main__':
    unittest.main()
