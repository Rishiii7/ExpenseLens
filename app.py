# app.py
import os
from flask import Flask, request, render_template
import sqlalchemy
from src.database import getconn, create_user_images_table, insert_user_image, closeConnection
from src.storage import upload_to_gcs
import certifi

app = Flask(__name__)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"credentials.json"
os.environ["SSL_CERT_FILE"] = certifi.where()

@app.route("/")
def home():
    # Redirect user to index page
    return render_template('verification.html')

@app.route('/upload_file', methods=['POST'])
def action_page():
    # Check if the post request has the file part
    if 'filename' not in request.files:
        print("File not found")
        # Handle the case where no file is selected
        return render_template('test.html', error="No file selected")

    # Get the uploaded file
    uploaded_file = request.files['filename']
    user_name = 'user_2'

    # Save the uploaded file to a local folder
    local_folder = 'Sample-Images/'
    if not os.path.exists(local_folder):
        os.makedirs(local_folder)

    file_name = uploaded_file.filename
    file_path = os.path.join(local_folder, file_name)
    uploaded_file.save(file_path)

    # Upload the file to Google Cloud Storage
    gcs_blob_name = f'{user_name}/{file_name}'  # Change the path as needed
    upload_to_gcs(file_path, gcs_blob_name)

    # create connection pool
    pool = sqlalchemy.create_engine(
        "postgresql+pg8000://",
        creator=getconn,
    )

    # create user_images table if not exists
    create_user_images_table(pool)

    # insert user and image details to PostgreSQL
    insert_user_image(pool, user_name, gcs_blob_name)

    # query database
    result = pool.execute(sqlalchemy.text("SELECT * from user_images")).fetchall()

    # Do something with the results
    for row in result:
        print(row)
    
    closeConnection()
    
    # Return a success message
    return render_template('ocr_success.html')

@app.route('/verify/<user_name>/<file_name>', methods=['GET', 'POST'])
def verify(user_name, file_name):
    # Retrieve user and image details from the database
    pool = sqlalchemy.create_engine(
        "postgresql+pg8000://",
        creator=getconn,
    )
    print(f"Connection established with the database")

    result = pool.execute(sqlalchemy.text("SELECT * FROM user_images WHERE username = :username AND image_path = :image_path"), 
                         {"username": user_name, "image_path": user_name+"/"+file_name}).fetchone()

    if result is None:
        # Handle the case where the record is not found
        print(f"The fetched result: {result}")

    # Extract the details for rendering on the verification page
    user_name = result['username']
    file_name = result['image_path']
    # Extract other fields as needed

    if request.method == 'POST':
        # Handle the form submission with corrected data
        corrected_data = {
            'merchant_name': request.form['merchant_name']
        }
        
        # update_user_image(pool, user_name, file_name, corrected_data)
        print(f"corrected_data: {corrected_data}")
        # Redirect to a success page or another action
        return render_template('verification_page.html')

    # Render the verification page
    return render_template('verification_page.html', user_name=user_name, file_name=file_name)


if __name__ == "__main__":
    app.run(debug=True)
