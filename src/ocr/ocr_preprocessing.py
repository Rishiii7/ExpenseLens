import json
import requests
import os
import sys

from ocr_utils import read_file_object
from dataclasses import dataclass

@dataclass
class ReceiptInfo:
        
    merchant_name :str 
    zip :int
    country :str
    state :str
    city :str
    date :str
    items :dict
    ocr_text :str


    def add_info_of_receipt(self, 
                            receipt :dict):
        print("Receipt into add function")

        self.merchant_name = receipt['ocr_text'].split('\n').strip()
        print(self.merchant_name)
        
        pass
    pass

class ReceiptProcessor:

    def __init__(self, file_path):
        self.file_path = file_path
        #self.Reciept_info_object = ReceiptInfo()

    def parse_json(self):
        raw_ocr_text = read_file_object(self.file_path, "r")
        # with open(self.file_path, 'r') as file:
        #     raw_ocr_text = json.load(file)
        return raw_ocr_text

    def extract_receipt_info(self, parsed_json):
        receipt = parsed_json['receipts'][0]
        merchant = receipt['ocr_text'].split('\n')[0].strip()
        location = {
            "city" : receipt['city'],
            "state" :receipt['state'],
            "country" : receipt['country'],
            "zip" : receipt['zip']
        }

        date = receipt['date']

        product_details = [ (item['description'],item['amount']) for item in receipt['items']]

        total_amount = receipt['total']
        sub_total_amount = receipt['subtotal']
        tax_amount = receipt['tax']

        payment_method = receipt['payment_method'] if receipt['payment_method']  else  "card"
        print(payment_method)
        print(product_details)
        print(merchant)
        #self.Reciept_info_object.add_info_of_receipt(receipt=receipt)
        
        return receipt

    def put_info_into_datbases(self):
        """
        after verficatiobn from user
        Call a database object
        that should redirect to database.py
        and insert the data into it
        
        """
        pass


    def print_receipt_info(self, receipt):
        print(f"Your purchase at {receipt['merchant_name']}")
        for item in receipt['items']:
            print(f" {item['description']} - ${item['amount']}")


if __name__ == "__main__":

    file_path = 'sample-response/response2.json' # change it to bucket path
    receipt_processor = ReceiptProcessor(file_path)
    parsed_json = receipt_processor.parse_json()
    receipt = receipt_processor.extract_receipt_info(parsed_json)
    receipt_processor.print_receipt_info(receipt)

