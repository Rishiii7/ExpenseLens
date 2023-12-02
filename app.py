# app.py
import os
from flask import Flask, request, render_template
import sqlalchemy
from src.database import getconn, create_user_images_table, insert_user_image, create_receipt_details_table, insert_receipt_details, closeConnection
from src.storage import upload_to_gcs
from src.ocr.ocr import *
from src.ocr.ocr_preprocessing import *
import certifi
import json

app = Flask(__name__)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"Credentials/credentials.json"
os.environ["SSL_CERT_FILE"] = certifi.where()
user_name = 'user'
image_name = ''

# create connection pool
pool = sqlalchemy.create_engine(
    "postgresql+pg8000://",
    creator=getconn,
)

def get_text_from_image(file_path : str):

    # running ocr.py code
    # ocr = AspriseOCR()
    # ocr_result = ocr.perform_ocr(file_path)
    # json_file_path = 'sample-response/response_'+file_path.split("/")[2]+'.json'
    json_file_path = 'sample-response/response3'+'.json'
    # write_file_object(json_file_path, "w", ocr_result)

    # running ocr_preprocessing.py code
    receipt_processor = ReceiptProcessor(json_file_path)
    parsed_json = receipt_processor.parse_json()
    receipt_info = receipt_processor.extract_receipt_info(parsed_json)
    receipt_processor.print_receipt_info(receipt_info)

    return receipt_info

@app.route("/")
def home():
    # Redirect user to index page
    return render_template('ocr_page.html')

@app.route('/upload_file', methods=['POST'])
def action_page():
    
    global image_name
    
    # Check if the post request has the file part
    if 'filename' not in request.files:
        print("File not found")
        # Handle the case where no file is selected
        return render_template('test.html', error="No file selected")

    # Get the uploaded file
    uploaded_file = request.files['filename']

    # Save the uploaded file to a local folder
    local_folder = 'static/Sample-Images/'
    if not os.path.exists(local_folder):
        os.makedirs(local_folder)

    file_name = uploaded_file.filename
    file_path = os.path.join(local_folder, file_name)
    uploaded_file.save(file_path)
    
    # Call the OCR API here to extract the info
    # from the image
    receipt_info = get_text_from_image(file_path)

    # Upload the file to Google Cloud Storage
    gcs_blob_name = f'{user_name}/{file_name}'  # Change the path as needed
    upload_to_gcs(file_path, gcs_blob_name)
        
    image_name = gcs_blob_name

    # create user_images table if not exists
    create_user_images_table(pool)

    # insert user and image details to PostgreSQL
    insert_user_image(pool, user_name, gcs_blob_name)

    # query database
    result = pool.execute(sqlalchemy.text("SELECT * from user_images")).fetchall()

    # Do something with the results
    for row in result:
        print(row)

    
    # Return a success message
    return render_template('verification-receipt-info.html', 
                           image_path= f"Sample-Images/" + file_name, 
                           receipt_info = receipt_info)

@app.route("/verify", methods = ["POST", "GET"])
def verify_receipt_info():

    category = request.form.get("category")
    merchant = request.form.get("merchant")
    zipcode = request.form.get("zipcode")
    country = request.form.get("country")
    state = request.form.get("state")
    city = request.form.get("city")
    date = request.form.get("date")
    total_amount = request.form.get("total_amount")
    sub_total_amount = request.form.get("sub_total_amount")
    tax = request.form.get("tax")
    items = request.form.get("items")

    # Now you can use the retrieved values as needed
    # For example, compare them with your own data and decide whether or not to process the transaction
    print(f"Merchant name: {merchant}")
    print(f"ZIP Code: {zipcode}")
    print(f"Country: {country}")
    print(f"State: {state}")
    print(f"City: {city}")
    print(f"Date: {date}")
    print(f"Total amount: {total_amount}")
    print(f"Sub-total amount: {sub_total_amount}")
    print(f"Tax: {tax}")
    print(f"Category: {category}")
    
    receipt_details = {
        "category" : category,
        "merchant_name" : merchant,
        "zip_code" : zipcode,
        "country" : country,
        "state" : state,
        "city" : city,
        "date" : date,
        "product_details" : json.dumps(items),
        "total_amount" : total_amount,
        "sub_total_amount" : sub_total_amount,
        "tax" : tax
    }
    
    # create receipt_details table if not exists
    create_receipt_details_table(pool)
    
    print(f"username: {user_name}")
    
    image_path = image_name
    
    print(f"image_path: {image_path}")
    # query database
    user_image_details = pool.execute(sqlalchemy.text("SELECT id from user_images WHERE username=:username and image_path=:image_path"), {"username": user_name, "image_path": image_path}).fetchall()
    user_id = user_image_details[0][0]
    print(f"user id : {user_id}")
    
    print(f"items: {items}")

    # to push updated receipt into
    #  SQL database
    insert_receipt_details(pool, user_id, receipt_details)
    
    # # # query database
    result = pool.execute(sqlalchemy.text("SELECT * from receipt_details")).fetchall()

    # # # Do something with the results
    for row in result:
        print(row)

    
    return render_template("ocr_success.html") 
    # Redirecting to dashboard


if __name__ == "__main__":
    app.run(
        debug=True
    )
