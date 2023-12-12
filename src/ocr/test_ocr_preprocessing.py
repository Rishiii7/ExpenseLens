# test_ocr_preprocessing.py
import unittest
from ocr_preprocessing import ReceiptProcessor, ReceiptInfo

class TestOCRPreprocessing(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Setup any necessary configurations for testing
        print("Setting up class-level resources or configurations")
        pass

    def setUp(self):
        # Setup any necessary test-specific configurations
        print("Setting up test-specific resources or configurations")
        pass

    def tearDown(self):
        # Clean up after each test
        print("Cleaning up resources or doing any necessary cleanup")
        pass

    def test_receipt_info_from_json(self):
        # Test the ReceiptInfo class method from_json
        json_data = {
            'ocr_text': 'Merchant Name\nZIP Code: 12345\nTotal: $100.0',
            'zip': 12345,
            'total': 100.0
        }
        receipt_info = ReceiptInfo.from_json(json_data)

        # Assertions based on your expectations
        self.assertEqual(receipt_info.merchant_name, 'Merchant Name')
        self.assertEqual(receipt_info.zip_code, 12345)
        self.assertEqual(receipt_info.total_amount, 100.0)

    def test_extract_receipt_info(self):
        # Test the ReceiptProcessor method extract_receipt_info

        # Create a mock OCR result
        ocr_result = {
            'receipts': [
                {
                    'ocr_text': 'Merchant Name\nZIP Code: 12345\nTotal: $100.0',
                    'zip': 12345,
                    'total': 100.0
                }
            ]
        }

        # Call the function you want to test
        receipt_processor = ReceiptProcessor(ocr_result)
        receipt_info = receipt_processor.extract_receipt_info()

        # Assertions based on your expectations
        self.assertEqual(receipt_info.merchant_name, 'Merchant Name')
        self.assertEqual(receipt_info.zip_code, 12345)
        self.assertEqual(receipt_info.total_amount, 100.0)

    def test_receipt_info_default_values(self):
        # Test that ReceiptInfo initializes with default values if not provided in the JSON
        json_data = {
            'ocr_text': 'Merchant Name',
        }
        receipt_info = ReceiptInfo.from_json(json_data)

        # Assertions based on your expectations for default values
        self.assertEqual(receipt_info.merchant_name, 'Merchant Name')
        self.assertEqual(receipt_info.zip_code, 0)
        self.assertEqual(receipt_info.total_amount, 0.0)

    def test_extract_receipt_info_multiple_receipts(self):
        # Test handling of multiple receipts in the OCR result
        ocr_result = {
            'receipts': [
                {
                    'ocr_text': 'Receipt 1\nTotal: $50.0',
                    'total': 50.0
                },
                {
                    'ocr_text': 'Receipt 2\nTotal: $75.0',
                    'total': 75.0
                }
            ]
        }

        receipt_processor = ReceiptProcessor(ocr_result)
        receipt_info = receipt_processor.extract_receipt_info()

        # Assertions based on your expectations
        # Assuming your implementation handles multiple receipts and returns info for the first one
        self.assertEqual(receipt_info.merchant_name, 'Receipt 1')
        self.assertEqual(receipt_info.total_amount, 50.0)

if __name__ == '__main__':
    unittest.main()
