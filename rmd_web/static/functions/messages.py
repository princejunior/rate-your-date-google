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
# MESSAGES
def get_messages():
    messages_ref = db.collection('messages').order_by('timestamp', direction=firestore.Query.DESCENDING).limit(10)
    messages = messages_ref.stream()
    return messages

def send_messages(user_id, message):
    db.collection('messages').add({
            'message': message,
            'user_id': user_id,
            'timestamp': firestore.SERVER_TIMESTAMP
        })

######################################################################################################################
