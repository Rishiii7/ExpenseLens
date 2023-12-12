import base64
import json
from flask import Flask, request, jsonify
from ocr import AspriseOCR
from ocr_preprocessing import ReceiptProcessor

# delete afterwaords
from ocr_utils import *

app_ocr = Flask(__name__)


@app_ocr.route('/perform_ocr', methods = ["POST"])
def perform_ocr():
    try :
        data = request.get_json()

        if 'image_base64' not in data :
            return jsonify({"error": "Missing image parameter"}), 400
        
        image_base64 = data['image_base64']
        image_bytes = base64.b64decode(image_base64)

        ocr = AspriseOCR()
        ocr_result = ocr.perform_ocr_from_bytes(image_bytes)

        # pre-processing of the ocr-result
        #### testing file 
        # ocr_result = read_file_object('sample-response/response3.json', "r")
        receipt_processor = ReceiptProcessor(ocr_result)
        print("##########################################  ")
        receipt_info = receipt_processor.extract_receipt_info()
        print("Receipt Info: ", receipt_info)
        receipt_processor.print_receipt_info(receipt_info)



        return jsonify({"receipt_info": receipt_info}), 200, {'Content-Type': 'application/json'}

    except Exception as e :
        return jsonify({'error' : str(e)}), 500


if __name__ == '__main__':
    app_ocr.run(port=5001)