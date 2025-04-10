import os
import boto3
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
BUCKET_NAME = os.getenv("BUCKET_NAME")
REGION = os.getenv("REGION")

app = Flask(__name__)

def upload_file_to_s3(file):
    s3 = boto3.client('s3',
                      aws_access_key_id=AWS_ACCESS_KEY,
                      aws_secret_access_key=AWS_SECRET_KEY,
                      region_name=REGION)
    s3.upload_fileobj(file, BUCKET_NAME, file.filename)
    return file.filename

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    filename = upload_file_to_s3(file)
    return jsonify({'filename': filename})

@app.route('/image/<filename>')
def image(filename):
    url = f"https://{BUCKET_NAME}.s3.{REGION}.amazonaws.com/{filename}"
    return jsonify({'url': url})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)