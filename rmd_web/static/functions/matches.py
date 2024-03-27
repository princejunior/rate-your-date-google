import firebase_admin
from firebase_admin import credentials, firestore, storage
from google.cloud.firestore_v1.base_query import FieldFilter
import datetime
from google.cloud.firestore_v1 import ArrayUnion
# Initialize Firebase Admin SDK
db = firestore.client()

######################################################################################################################
# MATCHES
def add_match(match_data):
    doc_ref = db.collection('matches').document()
    doc_ref.set({
        'userIds': match_data['userIds'],
        'timestamp': match_data['timestamp']
    })
    return doc_ref.id

def get_match(match_id):
    doc_ref = db.collection('matches').document(match_id)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    else:
        print(f"No match found with ID: {match_id}")
        return None

######################################################################################################################
