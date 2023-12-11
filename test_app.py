import unittest
from unittest.mock import MagicMock, patch
from flask import Flask
from app import app, login, verify_receipt_info, get_text_from_image, analytics

class TestApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Setup any necessary configurations for testing
        cls.app = app.test_client()

    def setUp(self):
        # Setup any necessary test-specific configurations
        pass

    def tearDown(self):
        # Clean up after each test
        pass

    def test_index_redirect(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, 'http://localhost/home')

    def test_home_route(self):
        response = self.app.get('/home')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_login_new_user(self):
        with patch('app.insert_authentication_details') as mock_insert:
            response = self.app.post('/login', data={'username': 'new_user', 'password': 'password'})
            mock_insert.assert_called_once()
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location, 'http://localhost/dashboard')

    def test_login_existing_user_success(self):
        with patch('app.pool.execute') as mock_execute:
            mock_execute.return_value.fetchall.return_value = [('hashed_password',)]
            response = self.app.post('/login', data={'username': 'existing_user', 'password': 'correct_password'})
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location, 'http://localhost/dashboard')

    def test_login_existing_user_failure(self):
        with patch('app.pool.execute') as mock_execute:
            mock_execute.return_value.fetchall.return_value = [('hashed_password',)]
            response = self.app.post('/login', data={'username': 'existing_user', 'password': 'incorrect_password'})
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location, 'http://localhost/home')
            self.assertIn(b'Login failed', response.data)

    def test_dashboard_route(self):
        with patch('app.analytics') as mock_analytics:
            response = self.app.get('/dashboard')
            mock_analytics.assert_called_once()
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Dashboard', response.data)

    def test_intermediate_route(self):
        response = self.app.get('/intermediate')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'OCR Page', response.data)

    def test_verify_receipt_info_route(self):
        with patch('app.insert_receipt_details') as mock_insert:
            response = self.app.post('/verify', data={'category': 'Grocery', 'merchant': 'Store', 'zipcode': '12345',
                                                       'country': 'US', 'state': 'CA', 'city': 'City', 'date': '2023-01-01',
                                                       'total_amount': '100.00', 'sub_total_amount': '90.00', 'tax': '10.00'})
            mock_insert.assert_called_once()
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location, 'http://localhost/dashboard')

    def test_upload_file_route(self):
        with patch('app.upload_to_gcs') as mock_upload:
            with patch('app.get_text_from_image') as mock_ocr:
                response = self.app.post('/upload_file', data={'filename': 'fake_image.jpg'})
                mock_upload.assert_called_once()
                mock_ocr.assert_called_once()
                self.assertEqual(response.status_code, 200)
                self.assertIn(b'Success', response.data)

    def test_get_text_from_image(self):
        with patch('app.requests.post') as mock_post:
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {'receipt_info': 'mocked_receipt_info'}
            result = get_text_from_image('fake_image.jpg')
            self.assertEqual(result, 'mocked_receipt_info')

    def test_get_text_from_image_error(self):
        with patch('app.requests.post') as mock_post:
            mock_post.return_value.status_code = 500
            mock_post.return_value.text = 'Error message'
            with self.assertRaises(Exception) as context:
                get_text_from_image('fake_image.jpg')
            self.assertEqual(str(context.exception), 'Error in OCR Server Response: Error message')


if __name__ == '__main__':
    unittest.main()
