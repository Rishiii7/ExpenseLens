import json
from ocr_utils import read_file_object
from dataclasses import dataclass

@dataclass
class ReceiptInfo:
    merchant_name: str
    zip_code: int
    country: str
    state: str
    city: str
    date: str
    items: list
    ocr_text: str
    total_amount: float
    sub_total_amount: float
    tax: float

    @classmethod
    def from_json(cls, receipt):
        merchant_name = receipt['ocr_text'].split('\n')[0].strip()
        return cls(
            merchant_name=merchant_name,
            zip_code=receipt.get('zip', 0),
            country=receipt.get('country', ''),
            state=receipt.get('state', ''),
            city=receipt.get('city', ''),
            date=receipt.get('date', ''),
            items=receipt.get('items', []),
            ocr_text=receipt.get('ocr_text', ''),
            total_amount=receipt.get('total', 0.0),
            sub_total_amount=receipt.get('subtotal', 0.0),
            tax=receipt.get('tax', 0.0)
        )

class ReceiptProcessor:

    def __init__(self, ocr_result):
        self.ocr_result = ocr_result

    def parse_json(self):
        return read_file_object(self.file_path, "r")

    def extract_receipt_info(self):
        print("*************************************")
        print(f"In ocr Preprocessing : {self.ocr_result}")
        receipt = self.ocr_result['receipts'][0]
        print(f"Recipts into OCR preprocessing : {receipt}")
        receipt_info = ReceiptInfo.from_json(receipt)

        # Additional processing if needed

        return receipt_info

    def print_receipt_info(self, receipt_info):
        print(f"Your purchase at {receipt_info.merchant_name}")
        print(f"Zipcode at {receipt_info.zip_code}")
        for item in receipt_info.items:
            print(f"{item['description']} - ${item['amount']}")
            
        print(f"Total amount : {receipt_info.total_amount}")

if __name__ == "__main__":
    file_path = 'sample-response/response3.json'  # Change it to the correct file path
    receipt_processor = ReceiptProcessor(file_path)
    parsed_json = receipt_processor.parse_json()
    receipt_info = receipt_processor.extract_receipt_info(parsed_json)
    receipt_processor.print_receipt_info(receipt_info)
