from app import app
from fastapi.testclient import TestClient
import unittest

class TestFastAPI(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_register_success(self):
        response = self.client.post("/register", data={"name": "John Doe", "email": "john@example.com", "role": "Developer"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"success": True})

    def test_register_failure(self):
        response = self.client.post("/register", data={"name": "John Doe", "email": "john@example.com"})
        self.assertEqual(response.status_code, 422)
        self.assertIn("detail", response.json())

    def test_register_invalid_email(self):
        response = self.client.post("/register", data={"name": "John Doe", "email": "invalid_email", "role": "Developer"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"success": False})

    def test_register_empty_fields(self):
        response = self.client.post("/register", data={"name": "", "email": "", "role": ""})
        self.assertEqual(response.status_code, 422)
        self.assertIn("detail", response.json())

if __name__ == "__main__":
    unittest.main()