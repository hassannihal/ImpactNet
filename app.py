"""
This Flask application serves as a backend for a web service that handles URL submissions and PDF uploads. It includes endpoints for:
- Submitting a URL which is then processed by an external method.
- Uploading PDF files which are then processed and split into images before uploading to Google Cloud Storage.
- Serving static files and the frontend index page.

The application uses Google Cloud Storage for file storage, processes URLs and PDFs through separate modules imported from subdirectories, and handles CORS (Cross-Origin Resource Sharing) settings for web security.

Environment variables are used to configure the application, including Google Cloud Storage bucket details and CORS policy.
"""
from flask import Flask, request, jsonify, send_from_directory
import os
import sys
from google.cloud import storage
from dotenv import load_dotenv

# Append paths for subdirectory imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend_url_method'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend_pdf_method'))

from split_pdf import split_pdf_and_upload
from main_url_method import process_url  # Importing function from backend_url_method
from main_pdf_method import main_pdf_method # Importing function from backend_pdf_method
from flask_cors import CORS

load_dotenv()
GCS_BUCKET = os.getenv('GCS_BUCKET')
cors = os.getenv('CORS')

# Initialize the Flask application and configure CORS
app = Flask(__name__, static_folder='frontend')
cors = CORS(app, resources={
    r"/*": {
        "origins": [cors]  # Specify the allowed origins
    }
})

# Ensure the directory for uploads exists
UPLOAD_FOLDER = 'upload-pdf/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # Limit file size to 100MB

@app.route('/submit-url', methods=['POST'])
def submit_url():
    """Handle URL submission, process the URL using process_url method."""
    url = request.form['url']
    if not url:
        return "No URL provided", 400
    # Use the imported function from backend_url_method
    process_url(url) #Process the URL
    return "URL processed successfully", 200

@app.route('/')
def index():
    """Serve the index page from the static folder."""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def send_static(path):
    """Serve static files from the static directory."""
    return send_from_directory(app.static_folder, path)

@app.route('/upload-pdf', methods=['POST'])
def upload_pdf():
    """Handle PDF file uploads and process them using main_pdf_method."""
    if 'pdf' not in request.files:
        return jsonify({'message': "No file part"}), 400
    file = request.files['pdf']
    if file.filename == '':
        return jsonify({'message': "No selected file"}), 400
    if file and file.filename.endswith('.pdf'):
        local_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(local_path)
        bucket_name = os.getenv('GCS_BUCKET')
        # Handle PDF processing, including optional splitting
        result = main_pdf_method(local_path, bucket_name)
        return jsonify({'message': "successfully uploaded"}), 200
    return jsonify({'message': "Invalid file type"}), 400    

if __name__ == '__main__':
    app.run(debug=True, port=3001)
