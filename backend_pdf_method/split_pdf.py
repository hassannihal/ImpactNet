import os
import fitz  # PyMuPDF
from google.cloud import storage
from save_strings_to_csv import save_to_csv

def upload_to_gcs(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    print(f"Uploaded {destination_blob_name} to bucket")
    # Construct and return the URI
    return f"gs://{bucket_name}/{destination_blob_name}"

def split_pdf_and_upload(file_path, bucket_name):
    """
    Converts a PDF file into images for each page, uploads each to Google Cloud Storage,
    and saves the resulting URIs to a CSV file.

    Args:
    file_path (str): The path to the PDF file to be converted.
    bucket_name (str): The name of the GCS bucket where files will be uploaded.

    Returns:
    list: A list of URIs corresponding to the uploaded images of PDF pages.
    """
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    uploaded_uris = []

    # Open the PDF file
    doc = fitz.open(file_path)

    for i in range(len(doc)):
        page = doc[i]
        pix = page.get_pixmap()
        image_filename = f"{file_name} - page {i + 1}.png"
        pix.save(image_filename)

        destination_blob_name = f"{file_name}/{file_name}-page-{i + 1}.png"
        uri = upload_to_gcs(bucket_name, image_filename, destination_blob_name)
        uploaded_uris.append(uri)

        os.remove(image_filename)
        print(f"Deleted local file: {image_filename}")

    doc.close()
    save_to_csv(uploaded_uris, "all_uri.csv")
    return uploaded_uris
