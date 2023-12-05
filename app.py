# app.py
import os
import sqlalchemy
import base64
from flask import Flask, request, render_template, redirect, url_for, flash
import requests
from src.database import getconn, create_user_images_table, insert_user_image, create_receipt_details_table, insert_receipt_details, create_authentication_table, insert_authentication_details, closeConnection
from src.storage import upload_to_gcs
import certifi
import json
import base64
from src.ocr.ocr_utils import *
import redis

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure secret key in a production environment

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"credentials.json"
os.environ["SSL_CERT_FILE"] = certifi.where()   
user_name = 'user'
image_name = ''

# redis_host = os.environ.get('REDIS_HOST', 'localhost')
# redis_port = os.environ.get('REDIS_PORT', '6379')
# redis_keys = {
#     "key1": "images",
#     "key2": "receiptDetails"
#     }

# create connection pool
pool = sqlalchemy.create_engine(
    "postgresql+pg8000://",
    creator=getconn,
)

# Redis configuration
# r = redis.StrictRedis(host=redis_host, port=redis_port, db=0)


# Dummy user credentials (in-memory storage)
users = {'user1': 'password1', 'user2': 'password2'}

OCR_SERVER_URL = 'http://localhost:5001'


def get_text_from_image(file_path : str):

    image_file = read_file_object(file_path, "rb")
    image_base64 = base64.b64encode(image_file).decode('utf-8')


    response = requests.post(
        f'{OCR_SERVER_URL}/perform_ocr',
        json={'image_base64' : image_base64}
    )

    print(response.text)

    if response.status_code == 200 :
        receipt_info = response.json().get('receipt_info')
        return receipt_info
    else :
        raise Exception(f"Error in OCR Server Response: {response.text}")

@app.route("/")
def index():
    return redirect(url_for('home'))

@app.route('/home')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    global user_name
    
    username = request.form.get('username')
    password = request.form.get('password')

    print(f"User name is : {username}")
    print(f"Password is : {password}")
    
    create_authentication_table(pool)
    
    result = pool.execute(sqlalchemy.text("SELECT * from authentication WHERE username = :username"),{"username": username}).fetchall()

    if not result:
        # Username doesn't exist, so insert the new username and password
        insert_authentication_details(pool, username, password)
        print("New user created successfully")
        
        user_name = username
        return redirect(url_for('dashboard'))
    else:
        # Username exists, check if the password matches
        stored_password = result[0][1]  # Assuming password is the second column in your authentication table
        if stored_password == password:
            print("Successful")
            user_name = username
            return redirect(url_for('dashboard'))
        else:
            print("Incorrect password")
            flash('Login failed. Please check your username and password.', 'error')
            return redirect(url_for('home'))


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/intermediate')
def intermediate():
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

    # This will be replaced by GCP sql code
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
    
    # # Pushing the user->image_path into cache
    # r.lpush(redis_keys['key1'], json.dumps({"user_name": user_name, "image_path": image_name}))
    
    # # Pushing the user->receipt_details into cache
    # r.lpush(redis_keys['key2'], json.dumps({"image_path": image_name, "receipt": receipt_info}))

    # create user_images table if not exists
    create_user_images_table(pool)

    # insert user and image details to PostgreSQL
    insert_user_image(pool, user_name, gcs_blob_name)

    # query database
    result = pool.execute(sqlalchemy.text("SELECT * from user_images")).fetchall()

    # Do something with the results
    for row in result:
        print(row)

    print(receipt_info['items'], '\n' ,type(receipt_info))

    # Return a succ ess message
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
    
    # user_details = r.blpop(redis_keys['key1'], 0)
    
    # receipt = r.blpop(redis_keys['key2'], 0)
    
    # user_details_json = json.loads(user_details[1].decode('utf-8'))
    # receipt_json = json.loads(receipt[1].decode('utf-8'))
    
    # print(f"user details from cache(before modification): {user_details_json}")
    
    # print(f"receipt details from cache(before modification): {receipt_json}")
    
    # receipt_json['receipt'] = receipt_details
    
    # # Pushing the user->image_path into cache
    # r.lpush(redis_keys['key1'], json.dumps(user_details_json))
    
    # # Pushing the user->receipt_details into cache
    # r.lpush(redis_keys['key2'], json.dumps(receipt_json))
    
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
    result = pool.execute(sqlalchemy.text("SELECT * from receipt_details_1")).fetchall()

    # # # Do something with the results
    for row in result:
        print(row)

    
    return render_template("ocr_success.html") 
    # Redirecting to dashboard


if __name__ == "__main__":
    app.run(
        debug=True
    )
