from App import app
import json
import unittest

class UsersTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        pass

    def test_get_all_users(self):
        response = self.app.get('/users')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)

    def test_get_user(self):
        response = self.app.get('/users/1')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, dict)
        self.assertEqual(data['id'], 1)

    def test_create_user(self):
        user = {
            'username': 'testuser',
            'password': 'password123',
            'email': 'testuser@example.com'
        }
        response = self.app.post('/users', json=user)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(data, dict)
        self.assertEqual(data['username'], user['username'])

    def test_update_user(self):
        user = {
            'username': 'testuser',
            'password': 'newpassword',
            'email': 'testuser@example.com'
        }
        response = self.app.put('/users/1', json=user)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, dict)
        self.assertEqual(data['password'], user['password'])

    def test_delete_user(self):
        response = self.app.delete('/users/1')

        self.assertEqual(response.status_code, 204)

if __name__ == '__main__':
    unittest.main()