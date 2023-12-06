import os
import base64
from flask import Flask, request, render_template, redirect, url_for, flash
import requests

from src.ocr.ocr_utils import *

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure secret key in a production environment

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
    return redirect(url_for('dashboard'))

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    print(f"User name is : {username}")
    print(f"Password is : {password}")

    # Check if the username and password match the stored credentials
    if username in users and users[username] == password:
        return render_template('ocr_page.html')
    else:
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

    print(receipt_info['items'], '\n' ,type(receipt_info))

    # Return a succ ess message
    return render_template('verification-receipt-info.html', 
                           image_path= f"Sample-Images/" + file_name, 
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
    item  =request.form.get("items")


    # Now you can use the retrieved values as needed
    # For example, compare them with your own data and decide whether or not to process the transaction
    print(f"Merchant name: {merchant}")
    print(f"ZIP Code: {zipcode}")
    print(f"Country: {country}")
    print(f"State: {state}")
    print(f"City: {city}")
    print(f"Date: {date}")
    print(f"Items: {item}")

    # to push updated receipt into
    #  SQL database
    return render_template("ocr_success.html") 
    # Redirecting to dashboard



if __name__ == "__main__":
    app.run(debug=True)

