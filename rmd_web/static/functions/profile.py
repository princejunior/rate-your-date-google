import firebase_admin
from firebase_admin import credentials, firestore, storage
from google.cloud.firestore_v1.base_query import FieldFilter
import datetime
from google.cloud.firestore_v1 import ArrayUnion
# from image_upload import image_upload
from . import image_upload
# Initialize Firebase Admin SDK
db = firestore.client()

######################################################################################################################
# PROFILE

def get_user_profile(user_id):
    doc_ref = db.collection('profiles').document(user_id)
    doc = doc_ref.get()
    if doc.exists:
        # print(doc.to_dict())
        return doc.to_dict()
    else:
        print(f"No user profile found for email: {user_id}")
        return None

def create_user_profile(user_profile_data):
    image_url = image_upload(user_profile_data['profile_picture'],"profile")
    doc_ref = db.collection('profiles').document(user_profile_data['email'])
    doc_ref.set({
        'first_name': user_profile_data['first_name'],
        'last_name': user_profile_data['last_name'],
        'profile_picture': image_url,
        'professional_background': user_profile_data['professional_background'],
        'social_media': user_profile_data['social_media'],
        'interests': user_profile_data['interests'],
        'privacy_settings': user_profile_data['privacy_settings']
    })

def edit_user_profile(user_id, updated_data):
    doc_ref = db.collection('profiles').document(user_id)
    doc_ref.update(updated_data)

def fetch_profile(profile_id):
    profile_ref = db.collection('profiles').document(profile_id)
    profile_data = profile_ref.get().to_dict()
    # print(profile_data)
    return profile_data
######################################################################################################################
