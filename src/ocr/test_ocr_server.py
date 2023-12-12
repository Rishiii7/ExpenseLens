# test_ocr_server.py
import unittest
from ocr_server import app_ocr
from unittest.mock import MagicMock, patch

class TestOCRServer(unittest.TestCase):

    def setUp(self):
        # Setup any necessary test-specific configurations before each test method runs
        self.app = app_ocr.test_client()

    def test_perform_ocr_success(self):
        # Test the perform_ocr endpoint with a successful OCR and pre-processing

        # Replace AspriseOCR.perform_ocr_from_bytes with a MagicMock for testing
        with patch('ocr_server.AspriseOCR.perform_ocr_from_bytes') as mock_perform_ocr:
            mock_perform_ocr.return_value = {'receipt_info': 'mocked_receipt_info'}

            # Mock the Flask request object
            image_base64 = 'mocked_image_base64'
            response = self.app.post('/perform_ocr', json={'image_base64': image_base64})

            # Assertions based on your expectations
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertEqual(data, {'receipt_info': 'mocked_receipt_info'})

    def test_perform_ocr_missing_image_param(self):
        # Test the perform_ocr endpoint with a missing image parameter

        # Mock the Flask request object without the 'image_base64' parameter
        response = self.app.post('/perform_ocr', json={})

        # Assertions based on your expectations
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data, {'error': 'Missing image parameter'})

    def test_perform_ocr_exception(self):
        # Test the perform_ocr endpoint when an exception occurs

        # Replace AspriseOCR.perform_ocr_from_bytes with a MagicMock for testing
        with patch('ocr_server.AspriseOCR.perform_ocr_from_bytes') as mock_perform_ocr:
            mock_perform_ocr.side_effect = Exception('mocked_exception')

            # Mock the Flask request object
            image_base64 = 'mocked_image_base64'
            response = self.app.post('/perform_ocr', json={'image_base64': image_base64})

            # Assertions based on your expectations
            self.assertEqual(response.status_code, 500)
            data = response.get_json()
            self.assertEqual(data, {'error': 'mocked_exception'})

if __name__ == '__main__':
    unittest.main()
