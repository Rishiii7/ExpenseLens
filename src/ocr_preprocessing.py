import json
import requests

with open('sample-response/response3.json', 'r') as file:
    raw_ocr_text = json.load(file)


#print(raw_ocr_text)
receipt = raw_ocr_text['receipts'][0]
print(f"Your purchase at {receipt['merchant_name']}")
for item in receipt['items']:
    print(f" {item['description']} - ${item['amount']}")
