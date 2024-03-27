import firebase_admin
from firebase_admin import credentials, firestore, storage
from google.cloud.firestore_v1.base_query import FieldFilter
import datetime
from google.cloud.firestore_v1 import ArrayUnion
# Initialize Firebase Admin SDK
db = firestore.client()


######################################################################################################################
# FEEDBACK
def add_feedback(feedback_data):
    doc_ref = db.collection('feedback').document()
    doc_ref.set({
        'from_user_id': feedback_data['fromUserId'],
        'toUserId': feedback_data['toUserId'],
        'content': feedback_data['content'],
        'timestamp': feedback_data['timestamp']
    })
    return doc_ref.id

def get_feedback(feedback_id):
    doc_ref = db.collection('feedback').document(feedback_id)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    else:
        print(f"No feedback found with ID: {feedback_id}")
        return None

######################################################################################################################
