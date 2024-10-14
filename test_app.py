"""
Test de integración
python -m unittest test_app.py
coverage run -m unittest test_app.py
"""

import unittest
import os
from app import app, crear_tabla, conectar_db

class FlaskTestCase(unittest.TestCase):
    """Test de integración"""

    def setUp(self):
        """Configuración inicial"""
        # Cambiar a modo de prueba
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()

        # Crear la base de datos de prueba
        self.db_path = 'test_database.db'
        app.config['DATABASE'] = self.db_path

        # Crear la tabla para pruebas
        crear_tabla()

    def tearDown(self):
        """Eliminar la base de datos de prueba después de cada test"""
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_crear_item(self):
        """Prueba: Crear un nuevo item (POST)"""
        response = self.app.post('/crear', data = {
            "nombre": 'Prueba item',
            "peso": '10kg',
            "tamano": 'Pequeño',
            "velocidad": '5 m/s'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Prueba item', response.data)

    def test_actualizar_item(self):
        """Prueba: Actualizar un item existente"""
        # Crear un item de prueba
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO items (nombre, peso, tamano, velocidad) VALUES (?, ?, ?, ?)",
            ('Item para actualizar', '15kg', 'Mediano', '10 m/s'))
        conn.commit()
        item_id = cursor.lastrowid
        conn.close()

        # Actualizar el item
        response = self.app.post(f'/actualizar/{item_id}', data= {
            "nombre": 'Item actualizado',
            "peso": '20kg',
            "tamano": 'Grande',
            "velocidad": '15 m/s'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Item actualizado', response.data)

    def test_eliminar_item(self):
        """Prueba: Eliminar un item"""
        # Crear un item de prueba
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO items (nombre, peso, tamano, velocidad) VALUES (?, ?, ?, ?)",
            ('Item para eliminar', '10kg', 'Pequeño', '7 m/s'))
        conn.commit()
        item_id = cursor.lastrowid
        conn.close()

        # Eliminar el item
        response = self.app.post(f'/eliminar/{item_id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Verificar que el item fue eliminado
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
        item = cursor.fetchone()
        conn.close()

        self.assertIsNone(item)

if __name__ == '__main__':
    unittest.main()
