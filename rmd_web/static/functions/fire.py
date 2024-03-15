import firebase_admin
from firebase_admin import credentials, firestore
# Initialize Firebase Admin SDK
db = firestore.client()

######################################################################################################################
# PROFILE

def get_user_profile(email):
    doc_ref = db.collection('user_profiles').document(email)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    else:
        print(f"No user profile found for email: {email}")
        return None

# # Example usage:
# user_email = 'example@example.com'
# user_profile = get_user_profile(user_email)
# if user_profile:
#     print("User Profile:")
#     print(user_profile)

def create_user_profile(user_profile_data):
    doc_ref = db.collection('user_profiles').document(user_profile_data['email'])
    doc_ref.set({
        'fullName': user_profile_data['fullName'],
        'profilePicture': user_profile_data['profilePicture'],
        'professionalBackground': user_profile_data['professionalBackground'],
        'interests': user_profile_data['interests'],
        'privacySettings': user_profile_data['privacySettings']
    })

def edit_user_profile(user_id, updated_data):
    doc_ref = db.collection('user_profiles').document(user_id)
    doc_ref.update(updated_data)

# # Example usage:
# user_email = 'example@example.com'
# updated_data = {
#     'fullName': 'Jane Doe',
#     'profilePicture': 'new_profile_pic.jpg',
#     'professionalBackground': ['Data Scientist'],
#     'interests': ['Cooking', 'Traveling', 'Photography'],
#     'privacySettings': {'email_visibility': 'public'}
# }
# edit_user_profile(user_email, updated_data)
######################################################################################################################

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

# # Example usage:
# match_data = {
#     'userIds': ['user1_id', 'user2_id'],
#     'timestamp': firestore.SERVER_TIMESTAMP
# }

# match_id = add_match(match_data)
# print("Match added with ID:", match_id)

# retrieved_match = get_match(match_id)
# if retrieved_match:
#     print("Retrieved Match:")
#     print(retrieved_match)
######################################################################################################################

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

# # Example usage:
# date_review_data = {
#     'reviewerId': 'user1_id',
#     'revieweeId': 'user2_id',
#     'rating': 4.5,
#     'comments': 'Had a great time!',
#     'timestamp': firestore.SERVER_TIMESTAMP,
#     'visibility': True
# }

# date_review_id = add_date_review(date_review_data)
# print("Date review added with ID:", date_review_id)

# retrieved_date_review = get_date_review(date_review_id)
# if retrieved_date_review:
#     print("Retrieved Date Review:")
#     print(retrieved_date_review)
######################################################################################################################

######################################################################################################################
# FEEDBACK
def add_feedback(feedback_data):
    doc_ref = db.collection('feedback').document()
    doc_ref.set({
        'fromUserId': feedback_data['fromUserId'],
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

# # Example usage:
# feedback_data = {
#     'fromUserId': 'user1_id',
#     'toUserId': 'user2_id',
#     'content': 'Great work!',
#     'timestamp': firestore.SERVER_TIMESTAMP
# }

# feedback_id = add_feedback(feedback_data)
# print("Feedback added with ID:", feedback_id)

# retrieved_feedback = get_feedback(feedback_id)
# if retrieved_feedback:
#     print("Retrieved Feedback:")
#     print(retrieved_feedback)
######################################################################################################################

######################################################################################################################
# GROUP_DATES
def add_group_date(group_date_data):
    doc_ref = db.collection('group_dates').document()
    doc_ref.set({
        'creator_id': group_date_data['creator_id'],
        'details': group_date_data['details'],
        'maxParticipants': group_date_data['maxParticipants'],
        'participants': group_date_data['participants'],
        'privacy': group_date_data['privacy'],
        'status': group_date_data['status'],
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

# # Example usage:
# group_date_data = {
#     'creator_id': 'example_creator_id',
#     'details': {
#         'date': '2024-03-20',
#         'time': '15:00',
#         'location': 'Central Park',
#         'interests': ['Hiking', 'Picnic']
#     },
#     'maxParticipants': 10,
#     'participants': ['user1_id', 'user2_id'],
#     'privacy': 'public',
#     'status': 'planned'
# }

# group_date_id = add_group_date(group_date_data)
# print("Group date added with ID:", group_date_id)

# retrieved_group_date = get_group_date(group_date_id)
# if retrieved_group_date:
#     print("Retrieved Group Date:")
#     print(retrieved_group_date)
######################################################################################################################
