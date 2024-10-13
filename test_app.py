# Test de integración
# python -m unittest test_app.py

import unittest
import sqlite3
import os
from app import app, crear_tabla, conectar_db

class FlaskTestCase(unittest.TestCase):
    # Configuración inicial
    def setUp(self):
        # Cambiar a modo de prueba
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()

        # Crear la base de datos de prueba
        self.db_path = 'test_database.db'
        app.config['DATABASE'] = self.db_path

        # Crear la tabla para pruebas
        crear_tabla()

    # Eliminar la base de datos de prueba después de cada test
    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    # Prueba: Crear un nuevo item (POST)
    def test_crear_item(self):
        response = self.app.post('/crear', data=dict(
            nombre='Prueba item',
            peso='10kg',
            tamano='Pequeño',
            velocidad='5 m/s'
        ), follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Prueba item', response.data)  # Verificar si el nuevo item se creó correctamente

    # Prueba: Actualizar un item existente
    def test_actualizar_item(self):
        # Crear un item de prueba
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO items (nombre, peso, tamano, velocidad) VALUES (?, ?, ?, ?)", ('Item para actualizar', '15kg', 'Mediano', '10 m/s'))
        conn.commit()
        item_id = cursor.lastrowid
        conn.close()

        # Actualizar el item
        response = self.app.post(f'/actualizar/{item_id}', data=dict(
            nombre='Item actualizado',
            peso='20kg',
            tamano='Grande',
            velocidad='15 m/s'
        ), follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Item actualizado', response.data)

    # Prueba: Eliminar un item
    def test_eliminar_item(self):
        # Crear un item de prueba
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO items (nombre, peso, tamano, velocidad) VALUES (?, ?, ?, ?)", ('Item para eliminar', '10kg', 'Pequeño', '7 m/s'))
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
