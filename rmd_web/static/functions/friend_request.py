import firebase_admin
from firebase_admin import firestore

def send_friend_request(sender_id, receiver_id):
    db = firestore.client()
    sender_ref = db.collection('users').document(sender_id)
    receiver_ref = db.collection('users').document(receiver_id)
    
    # Add sender_id to receiver's friend requests
    receiver_ref.update({
        'friend_requests': firestore.ArrayUnion([sender_id])
    })

def accept_friend_request(receiver_id, sender_id):
    db = firestore.client()
    receiver_ref = db.collection('users').document(receiver_id)
    sender_ref = db.collection('users').document(sender_id)
    
    # Remove sender_id from receiver's friend requests
    receiver_ref.update({
        'friend_requests': firestore.ArrayRemove([sender_id])
    })
    
    # Add receiver_id to sender's friends
    sender_ref.update({
        'friends': firestore.ArrayUnion([receiver_id])
    })

def reject_friend_request(receiver_id, sender_id):
    db = firestore.client()
    receiver_ref = db.collection('users').document(receiver_id)
    
    # Remove sender_id from receiver's friend requests
    receiver_ref.update({
        'friend_requests': firestore.ArrayRemove([sender_id])
    })
