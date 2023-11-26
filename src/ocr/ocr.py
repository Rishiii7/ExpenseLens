# ocr.py

import json
import requests
import sys

from ocr_utils import read_file_object, write_file_object

class AspriseOCR:
    def __init__(self, api_key='TEST'):
        self.api_key = api_key

    def perform_ocr(self, image_path, recognizer='auto', ref_no='oct_python_123'):
        """
        Performs Optical Character Recognition (OCR) on an image.

        :param image_path: Path to the image file.
        :param recognizer: The type of recognizer to use. Defaults to 'auto'.
        :param ref_no: A reference number for your OCR operation.
        :return: The OCR result as a JSON object.
        """

        receiptOcrEndpoint = 'https://ocr.asprise.com/api/v1/receipt'

        imageBytes = read_file_object(image_path, "rb")
        # with open(image_path, 'rb') as imageFile:
        #     imageBytes = imageFile.read()

        response = requests.post(url=receiptOcrEndpoint,
                                 data= {
                                     'api_key' : self.api_key,
                                     'recognizer' : recognizer,
                                     'ref_no' : ref_no
                                 },
                                 files= {
                                     'file' : imageBytes
                                 })

        if response.status_code == 200:
            return json.loads(response.text)
        else:
            raise Exception(f"Failed to perform OCR: {response.text}")


if __name__ == "__main__":
    # Test the class and method with a sample image
    ocr = AspriseOCR()
    ocr_result = ocr.perform_ocr('Sample-Images/Receipt1.jpeg')

    file_path = 'sample-response/response3.json'
    write_file_object(file_path, "w", ocr_result)
    # with open('sample-response/response3.json', "w") as f:
    #     json.dump(ocr_result, f)