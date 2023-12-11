# test_ocr.py
import unittest
from ocr import AspriseOCR
from unittest.mock import MagicMock, patch

class TestOCR(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Setup any necessary configurations for testing
        pass

    def setUp(self):
        # Setup any necessary test-specific configurations
        pass

    def tearDown(self):
        # Clean up after each test
        pass

    def test_perform_ocr_from_bytes_success(self):
        # Test the AspriseOCR method perform_ocr_from_bytes with a successful response

        # Replace requests.post with a MagicMock for testing
        with patch('requests.post') as mock_post:
            mock_post.return_value.status_code = 200
            mock_post.return_value.text = '{"receipt_info": "mocked_receipt_info"}'

            # Call the function you want to test
            ocr = AspriseOCR(api_key='TEST')
            result = ocr.perform_ocr_from_bytes(b'mocked_image_bytes')

            # Assertions based on your expectations
            self.assertEqual(result, {'receipt_info': 'mocked_receipt_info'})

    def test_perform_ocr_from_bytes_failure(self):
        # Test the AspriseOCR method perform_ocr_from_bytes with a failed response

        # Replace requests.post with a MagicMock for testing
        with patch('requests.post') as mock_post:
            mock_post.return_value.status_code = 500
            mock_post.return_value.text = '{"error": "mocked_error_message"}'

            # Call the function you want to test
            ocr = AspriseOCR(api_key='TEST')

            # Assertions based on your expectations
            with self.assertRaises(Exception) as context:
                ocr.perform_ocr_from_bytes(b'mocked_image_bytes')

            self.assertEqual(str(context.exception), 'Failed to perform OCR: mocked_error_message')

    def test_perform_ocr_from_bytes_invalid_json(self):
        # Test the AspriseOCR method perform_ocr_from_bytes with an invalid JSON response

        # Replace requests.post with a MagicMock for testing
        with patch('requests.post') as mock_post:
            mock_post.return_value.status_code = 200
            mock_post.return_value.text = 'invalid_json_response'

            # Call the function you want to test
            ocr = AspriseOCR(api_key='TEST')

            # Assertions based on your expectations
            with self.assertRaises(Exception) as context:
                ocr.perform_ocr_from_bytes(b'mocked_image_bytes')

            self.assertEqual(str(context.exception), 'Failed to perform OCR: invalid_json_response')

if __name__ == '__main__':
    unittest.main()
