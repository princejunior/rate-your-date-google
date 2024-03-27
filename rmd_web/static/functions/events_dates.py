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
# GROUP_DATES

def create_group_date(group_date_data):
    if group_date_data['image'] is not None:
        group_date_url_image = image_upload(group_date_data['image'], "group_dates")
    else:
        group_date_url_image = None
    doc_ref = db.collection('group_dates').document()
    doc_ref.set({
        'creator_id': group_date_data['creator_id'],
        'type_date_event': group_date_data['type_date_event'],
        'details': {
            'title': group_date_data['title'], 
            'image': group_date_url_image,
            # 'image': group_date_data['image'], 
            'about_date': group_date_data['about_date'],  
            'type': group_date_data['type'],
            'specifications': group_date_data['specifications'],
            'start_date': group_date_data['start_date'],
            'start_time': group_date_data['start_time'],
            'end_date': group_date_data['end_date'],
            'end_time': group_date_data['end_time'],
        },
        'maxParticipants': group_date_data['maxParticipants'],
        'participants': group_date_data['participants'],
        #friends/connections or for the public
        'privacy': group_date_data['privacy'],
        #expired or not expired
        'expired': group_date_data['expired'], 
    })
   # Update the profiles document by adding group date ID to the array
    profiles_ref = db.collection('profiles').document(group_date_data['creator_id'])
    profiles_ref.update({
        'events': ArrayUnion([doc_ref.id])
    })
    return doc_ref.id

def participated_group_date(group_date_data):
    # group_date_data = []
    #profile ids
    participants = [] 
    participants.append(group_date_data)
    
    doc_ref = db.collection('created_group_dates').document()

    doc_ref.set({
        'details': {
            'title': group_date_data['title'], 
            'image': group_date_data['image'],
            'image': group_date_data['image'], 
            'about_date': group_date_data['about_date'],  
            'type': group_date_data['type'],
            'specifications': group_date_data['specifications'],
            'start_date': group_date_data['start_date'],
            'start_time': group_date_data['start_time'],
            'end_date': group_date_data['end_date'],
            'end_time': group_date_data['end_time'],
        },
    })
    return doc_ref.id

def get_group_date(group_date_id):
    doc_ref = db.collection('group_dates').document(group_date_id)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    else:
        print(f"No group date found with ID: {group_date_id}")
        return None

def update_group_date(document_id, updated_data):
    db.collection('group_dates').document(document_id).update(updated_data)
    return f"Document with ID {document_id} updated successfully."

def delete_group_date(document_id):
    db.collection('group_dates').document(document_id).delete()
    return f"Document with ID {document_id} deleted successfully."

######################################################################################################################

######################################################################################################################
# EVENTS

def get_user_events(user_event_ids):
    events = []
    dates = []
    for event_id in user_event_ids:
        doc_ref = db.collection('group_dates').document(event_id)
        doc = doc_ref.get()
        if doc.exists:
            event_data = doc.to_dict()
            if event_data['type_date_event'] == 'Event':
                events.append(event_data)
            elif event_data['type_date_event'] == 'Date':
                dates.append(event_data)
            else:
                print(f"Unknown event type for event ID: {event_id}")
        else:
            print(f"No user event found for event ID: {event_id}")
    return events, dates

    

######################################################################################################################
