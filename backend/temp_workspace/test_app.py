
import unittest
from fastapi.testclient import TestClient
from your_module import app  # replace 'your_module' with the actual name of your module

class TestRegisterEndpoint(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_register_success(self):
        user_data = {
            "username": "test_user",
            "email": "test@example.com",
            "password": "test_password"
        }
        response = self.client.post('/register', json=user_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'success': True})

    def test_register_failure(self):
        user_data = {
            "username": "test_user",
            "email": "test@example.com"
        }
        response = self.client.post('/register', json=user_data)
        self.assertEqual(response.status_code, 422)

    def test_register_invalid_json(self):
        user_data = "invalid json"
        response = self.client.post('/register', data=user_data)
        self.assertEqual(response.status_code, 422)

if __name__ == '__main__':
    unittest.main()
