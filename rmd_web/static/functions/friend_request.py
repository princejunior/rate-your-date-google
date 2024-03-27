import firebase_admin
from firebase_admin import credentials, firestore, storage
from google.cloud.firestore_v1.base_query import FieldFilter
import datetime
from google.cloud.firestore_v1 import ArrayUnion
# Initialize Firebase Admin SDK
db = firestore.client()


######################################################################################################################
# FRIEND REQUESTS
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

    # # Get the friend requests array from sender's profile
    # friend_requests_sender = sender_profile.to_dict().get('friend_requests', [])
    # # Remove the friend request from sender's profile
    # friend_requests_sender = [req for req in friend_requests_sender if req['sender_email'] != sender_email or req['recipient_email'] != recipient_email]

    # # Update sender's profile with modified friend requests array
    # sender_ref.update({'friend_requests': friend_requests_sender})

    # # Get the friend requests array from recipient's profile
    # friend_requests_recipient = recipient_profile.to_dict().get('friend_requests', [])
    # # Remove the friend request from recipient's profile
    # friend_requests_recipient = [req for req in friend_requests_recipient if req['sender_email'] != sender_email or req['recipient_email'] != recipient_email]

    # # Update recipient's profile with modified friend requests array
    # recipient_ref.update({'friend_requests': friend_requests_recipient})

    # # Add each user to the other's friend list
    # sender_friends = sender_profile.to_dict().get('friends', [])
    # recipient_friends = recipient_profile.to_dict().get('friends', [])

    # # Add recipient to sender's friend list if not already present
    # if recipient_email not in sender_friends:
    #     sender_friends.append(recipient_email)
    #     sender_ref.update({'friends': sender_friends})

    # # Add sender to recipient's friend list if not already present
    # if sender_email not in recipient_friends:
    #     recipient_friends.append(sender_email)
    #     recipient_ref.update({'friends': recipient_friends})

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

    # # Get the friend requests array from sender's profile
    # friend_requests_sender = sender_profile.to_dict().get('friend_requests', [])
    # # Remove the friend request from sender's profile
    # friend_requests_sender = [req for req in friend_requests_sender if req['sender_email'] != sender_email or req['recipient_email'] != recipient_email]

    # # Update sender's profile with modified friend requests array
    # sender_ref.update({'friend_requests': friend_requests_sender})

    # # Get the friend requests array from recipient's profile
    # friend_requests_recipient = recipient_profile.to_dict().get('friend_requests', [])
    # # Remove the friend request from recipient's profile
    # friend_requests_recipient = [req for req in friend_requests_recipient if req['sender_email'] != sender_email or req['recipient_email'] != recipient_email]

    # # Update recipient's profile with modified friend requests array
    # recipient_ref.update({'friend_requests': friend_requests_recipient})

    return "Friend request declined successfully"
  
def get_user_friend_request(user_id):
    pass
######################################################################################################################
