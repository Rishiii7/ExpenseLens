import os
from flask import Flask, request, render_template, redirect

from src.ocr.ocr import *
from src.ocr.ocr_preprocessing import *

app = Flask(__name__)


def get_text_from_image(file_path : str):

    # running ocr.py code
    ocr = AspriseOCR()
    ocr_result = ocr.perform_ocr('Sample-Images/Receipt1.jpeg')
    json_file_path = 'sample-response/response3.json'
    write_file_object(json_file_path, "w", ocr_result)

    # running ocr_preprocessing.py code
    receipt_processor = ReceiptProcessor(json_file_path)
    parsed_json = receipt_processor.parse_json()
    receipt_info = receipt_processor.extract_receipt_info(parsed_json)
    receipt_processor.print_receipt_info(receipt_info)

    return receipt_info

@app.route("/")
def home():
    # # Redirect user to index page
    # json_file_path = 'sample-response/response3.json'
    # receipt_processor = ReceiptProcessor(json_file_path)
    # parsed_json = receipt_processor.parse_json()
    # receipt_info = receipt_processor.extract_receipt_info(parsed_json)
    # receipt_processor.print_receipt_info(receipt_info)

    

    return render_template('ocr_page.html')


@app.route('/upload_file', methods=['POST'])
def action_page():

    # Check if the post request has the file part
    if 'filename' not in request.files:
        print("File not found")
        # Handle the case where no file is selected
        return render_template('test.html', error="No file selected")

    # Get the uploaded file
    uploaded_file = request.files['filename']

    # Save the uploaded file to a local folder
    # Later we need to save the file into S3 buckets
    local_folder = 'static/Sample-Images/'
    if not os.path.exists(local_folder):
        os.makedirs(local_folder)

    # This will be replaced by GCP sql code
    file_name = uploaded_file.filename
    file_path = os.path.join(local_folder, file_name)
    uploaded_file.save(file_path)

    # Call the OCR API here to extract the info
    # from the image
    receipt_info = get_text_from_image(file_path)

    # print(ocr_info)


    # Return a success message
    return render_template('verification-receipt-info.html', 
                           file_path= f"Sample-Images/" + file_name, 
                           receipt_info = receipt_info)

@app.route("/verify", methods = ["POST", "GET"])
def verify_receipt_info():

    # Test This !!
    merchant = request.form.get("merchant")
    zipcode = request.form.get("zipcode")
    country = request.form.get("country")
    state = request.form.get("state")
    city = request.form.get("city")
    date = request.form.get("date")


    # Now you can use the retrieved values as needed
    # For example, compare them with your own data and decide whether or not to process the transaction
    print(f"Merchant name: {merchant}")
    print(f"ZIP Code: {zipcode}")
    print(f"Country: {country}")
    print(f"State: {state}")
    print(f"City: {city}")
    print(f"Date: {date}")

    # to push updated receipt into
    #  SQL database
    return render_template("ocr_success.html") 
    # Redirecting to dashboard



if __name__ == "__main__":
    app.run(debug=True)

