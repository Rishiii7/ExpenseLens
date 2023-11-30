import json
from src.ocr.ocr_utils import read_file_object
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
            ocr_text=receipt.get('ocr_text', '')
        )

class ReceiptProcessor:

    def __init__(self, file_path):
        self.file_path = file_path

    def parse_json(self):
        return read_file_object(self.file_path, "r")

    def extract_receipt_info(self, parsed_json):
        receipt = parsed_json['receipts'][0]
        receipt_info = ReceiptInfo.from_json(receipt)

        # Additional processing if needed

        return receipt_info

    def put_info_into_databases(self):
        """
        After verification from the user,
        call a database object that should redirect to database.py
        and insert the data into it.
        """
        pass

    def print_receipt_info(self, receipt_info):
        print(f"Your purchase at {receipt_info.merchant_name}")
        print(f"Zipcode at {receipt_info.zip_code}")
        for item in receipt_info.items:
            print(f"{item['description']} - ${item['amount']}")

if __name__ == "__main__":
    file_path = 'sample-response/response3.json'  # Change it to the correct file path
    receipt_processor = ReceiptProcessor(file_path)
    parsed_json = receipt_processor.parse_json()
    receipt_info = receipt_processor.extract_receipt_info(parsed_json)
    receipt_processor.print_receipt_info(receipt_info)
