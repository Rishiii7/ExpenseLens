import os
from flask import Flask, request, render_template, redirect


app = Flask(__name__)

@app.route("/")
def home():
    # Redirect user to index page
    return render_template('ocr_page.html')


@app.route('/upload_file', methods=['POST'])
def action_page():
    # Get the uploaded file
    uploaded_file = request.files['filename']

    # Save the uploaded file to a local folder
    # Later we need to save the file into S3 buckets
    local_folder = 'Sample-Images/'
    if not os.path.exists(local_folder):
        os.makedirs(local_folder)

    file_name = uploaded_file.filename
    file_path = os.path.join(local_folder, file_name)
    uploaded_file.save(file_path)

    print("Successfully uploaded the file")
    
    # Return a success message
    return render_template('ocr_success.html')


if __name__ == "__main__":
    app.run(debug=True)

