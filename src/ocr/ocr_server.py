import base64
import json
from flask import Flask, request, jsonify
import os
import redis

from ocr import AspriseOCR
from ocr_preprocessing import ReceiptProcessor
from ocr_utils import *

app_ocr = Flask(__name__)

redis_host = os.environ.get('REDIS_HOST', 'localhost')
redis_port = os.environ.get('REDIS_PORT', '6379')

# Redis configuration
r = redis.StrictRedis(host=redis_host, port=redis_port, db=0)

infoKey = "ocr.info"
debugKey = "ocr.debug"
def log_debug(message, key=debugKey):
    print("DEBUG:", message, file=sys.stdout)
    redisClient = redis.StrictRedis(host=redis_host, port=redis_port, db=0)
    redisClient.lpush('logging', f"{debugKey}:{message}")

def log_info(message, key=infoKey):
    print("INFO:", message, file=sys.stdout)
    redisClient = redis.StrictRedis(host=redis_host, port=redis_port, db=0)
    redisClient.lpush('logging', f"{infoKey}:{message}")

@app_ocr.route('/perform_ocr', methods = ["POST"])
def perform_ocr():
    log_info("Sucessfully data transmission from main flask application")
    try :
        data = request.get_json()

        if 'image_base64' not in data :
            log_debug("Missing image parameter in request.")
            return jsonify({"error": "Missing image parameter"}), 400
        
        image_base64 = data['image_base64']
        image_bytes = base64.b64decode(image_base64)

        ocr = AspriseOCR()
        ocr_result = ocr.perform_ocr_from_bytes(image_bytes)

        # pre-processing of the ocr-result
        #### testing file 
        # ocr_result = read_file_object('sample-response/response3.json', "r")
        receipt_processor = ReceiptProcessor(ocr_result)
        log_info("Performing OCR and extracting receipt information.")
        # print("##########################################  ")
        receipt_info = receipt_processor.extract_receipt_info()
        log_debug("Receipt Info: ", receipt_info)
        receipt_processor.print_receipt_info(receipt_info)



        return jsonify({"receipt_info": receipt_info}), 200, {'Content-Type': 'application/json'}

    except Exception as e :
        log_debug(f"Error during OCR processing: {str(e)}")
        return jsonify({'error' : str(e)}), 500


if __name__ == '__main__':
    app_ocr.run(port=5001)