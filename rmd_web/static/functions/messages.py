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
# Function to create a new conversation document
# def create_conversation(sender_id, recipient_id, last_message):
#     conversation_ref = db.collection("users").document(sender_id).collection("conversations").document()
#     conversation_ref.set({
#         "recipient_id": recipient_id,
#         "last_message": last_message,
#         "timestamp": firestore.SERVER_TIMESTAMP
#     })
#     print("Conversation document written with ID:", conversation_ref.id)
    
def get_messages(conversation_ids, current_user_id):
    # Reference to the "messages" collection
    messages_ref = db.collection('messages')

    # List to store all user messages
    all_user_messages = []
    all_other_users = []
    # Iterate over each user ID
    for conversation_id in conversation_ids:
        current_user_conversation = []
        other_user_conversation = []
        # Get document reference by ID
        doc_ref = messages_ref.document(conversation_id)

        # Get the document snapshot
        doc_snapshot = doc_ref.get()
        # print(doc_snapshot)
        
        # Check if the document exists
        if doc_snapshot.exists:
            # Get the data from the document
            doc_data = doc_snapshot.to_dict()
            # print(doc_data)

            # Extract user_1 and user_2 maps
            user_1 = doc_data.get('user_1', {})
            user_2 = doc_data.get('user_2', {})
            other_user_id = []
            # print('user_1', user_1)
            # print('user_2', user_2)
            
            # Determine the current user's role in the conversation
            if user_1.get('user_id') == current_user_id:
                # If the current user is user_1, set user_1_message to user_1's messages
                user_1_message = user_1.get('message_ids', [])
                user_2_message = user_2.get('message_ids', [])
                user_1_id = user_1.get('user_id', [])
                user_2_id = user_2.get('user_id', [])
                other_user_id.append(user_2_id)
                # Attach user_id to each dictionary in user_1_message
                for message in user_1_message:
                    message['user_id'] = user_1.get('user_id')
                    current_user_conversation.append(message)
                # Attach user_id to each dictionary in user_2_message
                for message in user_2_message:
                    message['user_id'] = user_2.get('user_id')
                    other_user_conversation.append(message)
                
            else:
                # If the current user is user_2, swap user_1 and user_2
                user_1_message = user_2.get('message_ids', [])
                user_2_message = user_1.get('message_ids', [])
                user_1_id = user_2.get('user_id', [])
                user_2_id = user_1.get('user_id', [])
                other_user_id.append(user_2_id)

                
                # Attach user_id to each dictionary in user_1_message
                for message in user_1_message:
                    message['user_id'] = user_1.get('user_id')
                    current_user_conversation.append(message)
                # Attach user_id to each dictionary in user_2_message
                for message in user_2_message:
                    message['user_id'] = user_2.get('user_id')
                    other_user_conversation.append(message)
                
                # print('current_user_conversation',current_user_conversation)
                # print('other_user_conversation',other_user_conversation)
            
            merge_coversations = current_user_conversation + other_user_conversation
            # print('merge_coversations',merge_coversations)
            sorted_messages = sorted(merge_coversations, key=lambda x: x['time_stamp'])
            # print('sorted messages',sorted_messages)

            # Construct conversation dictionary
            # conversation = {
            #     user_1_id: user_1_message,
            #     user_2_id: user_2_message
            # }
            
            # Append conversation to the list of all user messages
            # all_user_messages.append(conversation)
            all_user_messages.append(sorted_messages)
            all_other_users.append(other_user_id)
            
            
    return all_user_messages, other_user_id

# def get_messages(conversation_ids):
#     # Reference to the "messages" collection
#     messages_ref = db.collection('messages')

#     # List to store all user messages
#     all_user_messages = []

#     # Iterate over each user ID
#     for conversation_id in conversation_ids:
#         # Get document reference by ID
#         doc_ref = messages_ref.document(conversation_id)

#         # Get the document snapshot
#         doc_snapshot = doc_ref.get()
#         print(doc_snapshot)
        
#         # Check if the document exists
#         if doc_snapshot.exists:
#             # Get the data from the document
#             doc_data = doc_snapshot.to_dict()
#             print(doc_data)

#             # Extract user_1 and user_2 maps
#             user_1 = doc_data.get('user_1', {})
#             user_2 = doc_data.get('user_2', {})
#             print('user_1', user_1)
#             print('user_2', user_2)
            
#             # # Extract messages from user_1 and user_2
#             # Extract messages from user_1 and user_2
#             user_1_message = user_1.get('message_ids', [])
#             user_2_message = user_2.get('message_ids', [])
#             # print('user_1_message_ids',user_1_message)
#             # print('user_2_message_ids',user_2_message)
#             user_1_id = user_1.get('user_id', [])
#             user_2_id = user_2.get('user_id', [])
#             # Iterate over message IDs to retrieve messages
#             conversation = [
#                 {
#                     user_1_id: {
#                         user_1_message
#                     },
#                     user_2_id: {
#                         user_2_message
#                     }
#                 }
#             ]
        
#             # print('user_1_messages',user_1_messages)
#             # # Add messages to the list

#             print('conversation', conversation)
#     # return all_user_messages

def send_messages(message_id, user_id, message):
    # Check if message_id is None or empty
    if message_id is None or message_id == "":
        doc_ref = db.collection('messages').document()
    else:
        doc_ref = db.collection('messages').document(message_id)

    # Create a dictionary representing the message data
    message_data = {
        'user': user_id,
        'message': message,
        'timestamp': firestore.SERVER_TIMESTAMP
    }

    # Check if the document exists
    doc = doc_ref.get()

    if doc.exists:
        # If the document exists, update it by adding the message data to the messages array
        doc_ref.update({
            'messages': firestore.ArrayUnion([message_data])
        })
    else:
        # If the document doesn't exist, create it with the initial message data
        doc_ref.set({
            'messages': [message_data]  # Create a new array with the initial message data
        })
######################################################################################################################


# def send_messages(user_id, message,message_id):
#     db.collection('messages').add({
#             'message': message,
#             'user_id': user_id,
#             'timestamp': firestore.SERVER_TIMESTAMP
#         })
    