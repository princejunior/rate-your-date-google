import firebase_admin
from firebase_admin import credentials, firestore, storage
from google.cloud.firestore_v1.base_query import FieldFilter
import datetime
from google.cloud.firestore_v1 import ArrayUnion
# Initialize Firebase Admin SDK
db = firestore.client()

######################################################################################################################
# DATE_REVIEWS

def add_date_review(date_review_data):
    doc_ref = db.collection('date_reviews').document()
    doc_ref.set({
        'reviewerId': date_review_data['reviewerId'],
        'revieweeId': date_review_data['revieweeId'],
        'rating': date_review_data['rating'],
        'comments': date_review_data['comments'],
        'timestamp': date_review_data['timestamp'],
        'visibility': date_review_data['visibility']
    })
    return doc_ref.id

def get_date_review(date_review_id):
    doc_ref = db.collection('date_reviews').document(date_review_id)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    else:
        print(f"No date review found with ID: {date_review_id}")
        return None

######################################################################################################################
