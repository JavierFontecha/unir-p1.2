import http.client
import os
import unittest
from urllib.request import urlopen
from urllib.error import HTTPError


import pytest

BASE_URL = "http://localhost:5000"
BASE_URL_MOCK = "http://localhost:9090"
DEFAULT_TIMEOUT = 2  # in secs

@pytest.mark.api
class TestApi(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(BASE_URL, "URL no configurada")
        self.assertTrue(len(BASE_URL) > 8, "URL no configurada")

    def test_api_add(self):
        url = f"{BASE_URL}/calc/add/1/2"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        self.assertEqual(
            response.read().decode(), "3", "ERROR ADD"
        )

    def test_api_sqrt(self):
        url = f"{BASE_URL_MOCK}/calc/sqrt/64"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        self.assertEqual(
            response.read().decode(), "8", "ERROR SQRT"
        )
    
    def test_api_multiply(self):
        url = f"{BASE_URL_MOCK}/calc/multiply/2/3"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        self.assertEqual(
            response.read().decode(), "6", "ERROR MULTIPLY"
        )
    
    def test_api_divide(self):
        url = f"{BASE_URL_MOCK}/calc/divide/2/2"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        self.assertEqual(
            response.read().decode(), "1", "ERROR DIVIDE"
        )
        
    def test_api_divide_cero(self):
        url = f"{BASE_URL_MOCK}/calc/divide/2/0"
        try:
            response = urlopen(url, timeout=DEFAULT_TIMEOUT)
            self.fail(f"Se esperaba un error HTTP pero la respuesta fue: {response.status}")
        except HTTPError as e:
            # Verificamos http 406
            self.assertEqual(
                e.code,
                http.client.NOT_ACCEPTABLE,
                f"Se esperaba un código 406 pero se recibió {e.code} al llamar a {url}"
            )
            self.assertEqual(
                e.read().decode(),
                "Division by zero is not allowed",
                "El mensaje de error no coincide con lo esperado"
            )


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
