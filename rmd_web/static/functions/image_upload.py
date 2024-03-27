import firebase_admin
from firebase_admin import credentials, firestore, storage
from google.cloud.firestore_v1.base_query import FieldFilter
import datetime
from google.cloud.firestore_v1 import ArrayUnion
# Initialize Firebase Admin SDK
db = firestore.client()

######################################################################################################################
# UPLOAD_IMAGE

def image_upload(uploaded_image,folder):
    # print('upload_image',uploaded_image)
    # print('upload_image.name',uploaded_image.name)
    
    bucket = storage.bucket()
    blob = bucket.blob(folder+ '/' + uploaded_image.name)  # Replace with the desired path and name for the uploaded image in Firebase Storage
    blob.upload_from_file(uploaded_image)
    # Set expiration time to datetime.max
    expiration_time = datetime.datetime.max
    # Generate signed URL with expiration time set to datetime.max
    download_url = blob.generate_signed_url(expiration_time, method='GET')
    print(f"Image uploaded successfully. Download URL: {download_url}")
    return download_url
  
######################################################################################################################
