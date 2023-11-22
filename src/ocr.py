# import libraries
import json
import requests

receiptOcrEndpoint = 'https://ocr.asprise.com/api/v1/receipt'

# Later to be replaced by AWS S3 Bucket link
# include libarires regarding that

# Load the image file to analyze
with open('Sample-Images/Receipt1.jpeg', 'rb') as imageFile:
    imageBytes = imageFile.read()

# Make a POST request with the image bytes in the body of the request
response = requests.post(url=receiptOcrEndpoint,
                         data= {
                             'api_key' : 'TEST',
                             'recognizer' : 'auto',
                             'ref_no' : 'oct_python_123'
                         },
                         files= {
                             'file' : imageBytes
                         })


# Check if the response was successful and print out the result
with open('sample-response/response2.json', "w") as f:
    json.dump(json.loads(response.text), f)