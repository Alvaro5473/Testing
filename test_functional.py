"""
Test funcional
python test_functional.py
coverage run test_functional.py
"""

import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By

class FunctionalTest(unittest.TestCase):
    """Test funcional"""

    @classmethod
    def setUpClass(cls):
        # Configurar el driver del navegador (por ejemplo, Chrome)
        cls.driver = webdriver.Chrome()
        cls.driver.get('http://127.0.0.1:5000/')

    @classmethod
    def tearDownClass(cls):
        """Cerrar el navegador después de que todos los tests se ejecuten"""
        cls.driver.quit()

    def test_crear_nuevo_item(self):
        """Test: Crear un nuevo item"""

        driver = self.driver

        # Navegar a la página de creación de un nuevo item
        driver.find_element(By.LINK_TEXT, 'Crear nuevo item').click()

        # Rellenar el formulario
        nombre_input = driver.find_element(By.NAME, 'nombre')
        nombre_input.send_keys('Item funcional')

        peso_input = driver.find_element(By.NAME, 'peso')
        peso_input.send_keys('25kg')

        tamano_input = driver.find_element(By.NAME, 'tamano')
        tamano_input.send_keys('Grande')

        velocidad_input = driver.find_element(By.NAME, 'velocidad')
        velocidad_input.send_keys('15 m/s')

        # Enviar el formulario
        driver.find_element(By.XPATH, "//button[@type='submit']").click()

        # Esperar un momento para que se procese la redirección
        time.sleep(2)

        # Comprobar que el nuevo item aparece en la página principal
        self.assertIn("Item funcional", driver.page_source)

if __name__ == '__main__':
    unittest.main()
