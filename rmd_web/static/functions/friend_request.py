import firebase_admin
from firebase_admin import credentials, firestore, storage
from google.cloud.firestore_v1.base_query import FieldFilter
import datetime
from google.cloud.firestore_v1 import ArrayUnion
# Initialize Firebase Admin SDK
db = firestore.client()


######################################################################################################################
# FRIEND REQUESTS
def get_friend_request(user_data):
    pass


def send_friend_request(sender_id, recipient_id ):
    # Specify the document reference
    print('inside send_friend_request', recipient_id)
    
    # Get a reference to the "friend_requests" collection and generate a new document ID
    friend_requests_ref = db.collection('friend_requests').document()

    # Set the data for the friend request
    friend_requests_ref.set({
        'sender_id': sender_id,
        'recipient_id': recipient_id,
        'status': 'pending'
    })
    friend_request_id = friend_requests_ref.id
    
    sender_friend_requests_ref = db.collection('profiles').document(sender_id)
    sender_friend_requests_ref.update({
        'sent_friend_requests': firestore.ArrayUnion([friend_request_id])
    })
    
    recipient_profile_ref = db.collection('profiles').document(recipient_id)
    # Update the friend_requests field by appending the new friend request document ID
    recipient_profile_ref.update({
        'friend_requests': firestore.ArrayUnion([friend_request_id])
    })

def accept_friend_request(sender_email, recipient_email):
    # Reference to the sender's profile document
    sender_ref = db.collection('profiles').document(sender_email)

    # Reference to the recipient's profile document
    recipient_ref = db.collection('profiles').document(recipient_email)

    # Retrieve the sender's profile document
    sender_profile = sender_ref.get()
    if not sender_profile.exists:
        return "Sender profile not found"

    # Retrieve the recipient's profile document
    recipient_profile = recipient_ref.get()
    if not recipient_profile.exists:
        return "Recipient profile not found"
    return "Friend request accepted successfully"
 
def decline_friend_request(sender_id, recipient_id):
    # Reference to the sender's profile document
    sender_ref = db.collection('profiles').document(sender_id)

    # Reference to the recipient's profile document
    recipient_ref = db.collection('profiles').document(recipient_id)

    # Retrieve the sender's profile document
    sender_profile = sender_ref.get()
    if not sender_profile.exists:
        return "Sender profile not found"

    # Retrieve the recipient's profile document
    recipient_profile = recipient_ref.get()
    if not recipient_profile.exists:
        return "Recipient profile not found"

    return "Friend request declined successfully"
  
def get_user_friend_request(user_id):
    pass
######################################################################################################################
