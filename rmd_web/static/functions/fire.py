import firebase_admin
from firebase_admin import credentials, firestore, storage
from google.cloud.firestore_v1.base_query import FieldFilter
import datetime
# Initialize Firebase Admin SDK
db = firestore.client()

######################################################################################################################
# PROFILE

def get_user_profile(user_id):
    doc_ref = db.collection('profiles').document(user_id)
def get_user_profile(email):
    doc_ref = db.collection('profiles').document(email)
    doc = doc_ref.get()
    if doc.exists:
        print(doc.to_dict())
        return doc.to_dict()
    else:
        print(f"No user profile found for email: {user_id}")
        return None

# # Example usage:
# user_email = 'example@example.com'
# user_profile = get_user_profile(user_email)
# if user_profile:
#     print("User Profile:")
#     print(user_profile)

def create_user_profile(user_profile_data):
    image_url = image_upload(user_profile_data['profile_picture'],"profile")
    doc_ref = db.collection('profiles').document(user_profile_data['email'])
    doc_ref.set({
        'first_name': user_profile_data['first_name'],
        'last_name': user_profile_data['last_name'],
        'profile_picture': image_url,
        'professional_background': user_profile_data['professional_background'],
        'social_media': user_profile_data['social_media'],
        'interests': user_profile_data['interests'],
        'privacy_settings': user_profile_data['privacy_settings']
    })

def edit_user_profile(user_id, updated_data):
    doc_ref = db.collection('profiles').document(user_id)
    doc_ref = db.collection('profiles').document(user_id)
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
# group_date_id = add_group_date(group_date_data)
# print("Group date added with ID:", group_date_id)
# group_date_id = add_group_date(group_date_data)
# print("Group date added with ID:", group_date_id)

# retrieved_group_date = get_group_date(group_date_id)
# if retrieved_group_date:
#     print("Retrieved Group Date:")
#     print(retrieved_group_date)
######################################################################################################################

######################################################################################################################
# UPLOAD_IMAGE

def image_upload(uploaded_image,folder):
    print(uploaded_image)
def image_upload(uploaded_image):
    print(uploaded_image)
    bucket = storage.bucket()
    blob = bucket.blob(folder+ '/' + uploaded_image.name)  # Replace with the desired path and name for the uploaded image in Firebase Storage
    blob.upload_from_file(uploaded_image)
    # blob = bucket.blob('path/to/image.jpg')  # Replace with the desired path and name for the image in Firebase Storage
    # blob.upload_from_filename('path/to/local/image.jpg')  # Replace with the actual path of the local image file
    # download_url = blob.generate_signed_url(datetime.timedelta(seconds=300), method='GET')


    # Set expiration time to datetime.max
    expiration_time = datetime.datetime.max

    # Generate signed URL with expiration time set to datetime.max
    download_url = blob.generate_signed_url(expiration_time, method='GET')

    # download_url = blob.generate_signed_url(datetime.timedelta(seconds=300), method='GET')


    # Set expiration time to datetime.max
    expiration_time = datetime.datetime.max
    # Generate signed URL with expiration time set to datetime.max
    download_url = blob.generate_signed_url(expiration_time, method='GET')
    print(f"Image uploaded successfully. Download URL: {download_url}")
    return download_url
  
######################################################################################################################

######################################################################################################################
# POSTS
def get_user_post(user_id):
    # Assuming you're using the Firestore client library
    doc_ref = db.collection('posts').where('target_user_id', '==', user_id)
    docs = doc_ref.stream()

    posts = []
    for doc in docs:
        if doc.exists:
            post_data = doc.to_dict()
            post_data['id'] = doc.id  # Assuming the post ID is stored in 'id' field in Firestore
            posts.append(post_data)

    if not posts:
        print(f"No user post found for user_id: {user_id}")
        return []

    # Sort posts by timestamp in descending order (most recent first)
    posts.sort(key=lambda x: x['timestamp'], reverse=True)
    
    return posts

def get_friends_posts(friends_ids):
    all_posts = []
    
    for friend_id in friends_ids:
        # Assuming you're using the Firestore client library
        doc_ref = db.collection('posts').where('target_user_id', '==', friend_id)
        docs = doc_ref.stream()

        posts = []
        for doc in docs:
            if doc.exists:
                post_data = doc.to_dict()
                post_data['id'] = doc.id  # Assuming the post ID is stored in 'id' field in Firestore
                posts.append(post_data)

        if posts:
            all_posts.extend(posts)

    if not all_posts:
        print("No posts found for any of the friends.")
        return []

    # Sort all posts by timestamp in descending order (most recent first)
    all_posts.sort(key=lambda x: x['timestamp'], reverse=True)
    
    return all_posts

# def get_friends_posts(friends_id):
    
#      # Assuming you're using the Firestore client library
#     doc_ref = db.collection('posts').where('target_user_id', '==', friend_id)
#     docs = doc_ref.stream()

#     posts = []
#     for doc in docs:
#         if doc.exists:
#             post_data = doc.to_dict()
#             post_data['id'] = doc.id  # Assuming the post ID is stored in 'id' field in Firestore
#             posts.append(post_data)

#     if not posts:
#         print(f"No user post found for user_id: {friend_id}")
#         return []

#     # Sort posts by timestamp in descending order (most recent first)
#     posts.sort(key=lambda x: x['timestamp'], reverse=True)
    
#     return posts
    
# def get_user_post(user_id):
#     # Assuming you're using the Firestore client library
#     doc_ref = db.collection('posts').where('target_user_id', '==', user_id)
#     docs = doc_ref.stream()

#     for doc in docs:
#         if doc.exists:
#             return doc.to_dict()

#     print(f"No user post found for email: {user_id}")
#     return None

# Function to add a post to Firestore
def add_post(user_id, target_user_id, post_content, post_image_url=None):
    print("inside add_post")
    # Create a new document in the "posts" collection
    doc_ref = db.collection("posts").document()
    if post_image_url is not None:
        post_url_image = image_upload(post_image_url, "post")
    else:
        post_url_image = None
    
    new_post_ref = db.collection('posts').document()
    # Define the data for the post
    new_post_ref.set({
        "user_id": user_id,
        "target_user_id": target_user_id,
        "post_content": post_content,
        "post_image_url": post_url_image,
        "likes": 0,
        "dislikes": 0,
        "comments": [],
        "timestamp": firestore.SERVER_TIMESTAMP
    })
    
    # Set the data for the document
    # doc_ref.set(new_post_ref)
    print("Post added successfully")
    print("Out of add_post")
    

# Function to add a comment to a post
def add_comment(post_id, user_id, target_user_id, comment_content):
    # Reference the post document
    post_ref = db.collection("posts").document(post_id)
    
    # Get the current comments list
    post_data = post_ref.get().to_dict()
    comments = post_data.get("comments", [])
    
    # Add the new comment
    new_comment = {
        "user_id": user_id,
        "target_user_id": target_user_id,
        "comment_content": comment_content,
        "timestamp": firestore.SERVER_TIMESTAMP
    }
    comments.append(new_comment)
    
    # Update the comments field in the document
    post_ref.update({"comments": comments})
    print("Comment added successfully")

# Function to like a post
def like_post(post_id, current_user_id):
    print("inside like_post()")
    
    # Reference the post document
    post_ref = db.collection("posts").document(post_id)
    
    # Atomically increment likes by 1
    post_ref.update({"likes": firestore.Increment(1)})
    
    # Add the user to the list of users who liked the post
    # post_ref.collection("likes").add({"user_id": current_user_id})
    
    print("Post liked")
    print("finished like_post()")
    

# Function to dislike a post
def dislike_post(post_id, current_user_id):
    # Reference the post document
    post_ref = db.collection("posts").document(post_id)
    
    # Atomically increment dislikes by 1
    post_ref.update({"dislikes": firestore.Increment(1)})
    
    # Add the user to the list of users who disliked the post
    # post_ref.collection("dislikes").add({"user_id": current_user_id, "target_user_id": target_user_id})
    
    print("Post disliked")

    
    
######################################################################################################################

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

######################################################################################################################
# SEARCH
def search_profiles_single_term(term):
    # Searches for profiles based on a single search term.

    # Args:
    #     term (str): The search term (e.g., "John" or "example@email.com").

    # Returns:
    #     list: List of profile documents matching the search term.
    
    print("term:", term)
    profiles_ref = db.collection("profiles")

     # Construct the query dynamically for all specified fields
    # for field in ["first_name", "last_name", "email"]:
    #     filter = FieldFilter(field, "==", term)
    #     profiles_ref = profiles_ref.where(filter=filter)
    id_ref = profiles_ref.where(filter=FieldFilter("id", "==", term))
    first_name_ref = profiles_ref.where(filter=FieldFilter("first_name", "==", term))
    last_name_ref = profiles_ref.where(filter=FieldFilter("last_name", "==", term))
    email_ref = profiles_ref.where(filter=FieldFilter("email", "==", term))
    
    
    
    # profiles_ref = profiles_ref.where("first_name", "==", "e")

    # Execute the query
    # results = profiles_ref.stream()
    # profiles = []
    # for profile in results:
    #     profiles.append(profile.to_dict())
    id_results = id_ref.stream()
    first_name_results = first_name_ref.stream()
    last_name_results = last_name_ref.stream()
    email_results = email_ref.stream()
    
    # profiles = []
    # for profile in id_results:
    #     profiles.append(profile.to_dict())
    # for profile in first_name_results:
    #     profiles.append(profile.to_dict())
    # for profile in last_name_results:
    #     profiles.append(profile.to_dict())
    # for profile in email_results:
    #     profiles.append(profile.to_dict())
    
    profiles = []

    # Add profiles from id_results
    for profile in id_results:
        profile_dict = profile.to_dict()
        if profile_dict not in profiles:
            profiles.append(profile_dict)

    # Add profiles from first_name_results
    for profile in first_name_results:
        profile_dict = profile.to_dict()
        if profile_dict not in profiles:
            profiles.append(profile_dict)

    # Add profiles from last_name_results
    for profile in last_name_results:
        profile_dict = profile.to_dict()
        if profile_dict not in profiles:
            profiles.append(profile_dict)

    # Add profiles from email_results
    for profile in email_results:
        profile_dict = profile.to_dict()
        if profile_dict not in profiles:
            profiles.append(profile_dict)

        
    # Collect the matching profiles
    # profiles = remove_duplicates(profiles)

    # print('profiles', profiles)
    return profiles



def search_profiles(query):
   
    # Searches for profiles based on the provided query.

    # Args:
    #     query (dict): A dictionary containing search parameters (e.g., {"first_name": "John"}).

    # Returns:
    #     list: List of profile documents matching the query.
 
    profiles_ref = db.collection("profiles")

    # Construct the query dynamically based on the provided parameters
    for field, value in query.items():
        profiles_ref = profiles_ref.where(field, "==", value)

    # Execute the query
    results = profiles_ref.stream()

    # Collect the matching profiles
    profiles = []
    for profile in results:
        profiles.append(profile.to_dict())

    return profiles

######################################################################################################################

######################################################################################################################
# FRIEND REQUESTS
def send_friend_request(sender_id, recipient_id ):
    # Specify the document reference
    print('inside send_friend_request', recipient_id)
    friend_requests_ref = db.collection('profiles').document(recipient_id)

# Update the array field
    friend_requests_ref.update({
        'friend_requests': firestore.ArrayUnion([{
            'sender_id': sender_id,
            'recipient_id': recipient_id,
            'status': 'pending'
        }])
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

    # Get the friend requests array from sender's profile
    friend_requests_sender = sender_profile.to_dict().get('friend_requests', [])
    # Remove the friend request from sender's profile
    friend_requests_sender = [req for req in friend_requests_sender if req['sender_email'] != sender_email or req['recipient_email'] != recipient_email]

    # Update sender's profile with modified friend requests array
    sender_ref.update({'friend_requests': friend_requests_sender})

    # Get the friend requests array from recipient's profile
    friend_requests_recipient = recipient_profile.to_dict().get('friend_requests', [])
    # Remove the friend request from recipient's profile
    friend_requests_recipient = [req for req in friend_requests_recipient if req['sender_email'] != sender_email or req['recipient_email'] != recipient_email]

    # Update recipient's profile with modified friend requests array
    recipient_ref.update({'friend_requests': friend_requests_recipient})

    # Add each user to the other's friend list
    sender_friends = sender_profile.to_dict().get('friends', [])
    recipient_friends = recipient_profile.to_dict().get('friends', [])

    # Add recipient to sender's friend list if not already present
    if recipient_email not in sender_friends:
        sender_friends.append(recipient_email)
        sender_ref.update({'friends': sender_friends})

    # Add sender to recipient's friend list if not already present
    if sender_email not in recipient_friends:
        recipient_friends.append(sender_email)
        recipient_ref.update({'friends': recipient_friends})

    return "Friend request accepted successfully"
 
def decline_friend_request(sender_email, recipient_email):
    # Initialize Firestore client
    db = firestore.Client()

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

    # Get the friend requests array from sender's profile
    friend_requests_sender = sender_profile.to_dict().get('friend_requests', [])
    # Remove the friend request from sender's profile
    friend_requests_sender = [req for req in friend_requests_sender if req['sender_email'] != sender_email or req['recipient_email'] != recipient_email]

    # Update sender's profile with modified friend requests array
    sender_ref.update({'friend_requests': friend_requests_sender})

    # Get the friend requests array from recipient's profile
    friend_requests_recipient = recipient_profile.to_dict().get('friend_requests', [])
    # Remove the friend request from recipient's profile
    friend_requests_recipient = [req for req in friend_requests_recipient if req['sender_email'] != sender_email or req['recipient_email'] != recipient_email]

    # Update recipient's profile with modified friend requests array
    recipient_ref.update({'friend_requests': friend_requests_recipient})

    return "Friend request declined successfully"
  
def get_user_friend_request(user_id):
    pass
######################################################################################################################

######################################################################################################################
# 

######################################################################################################################

######################################################################################################################
# 

######################################################################################################################

######################################################################################################################
# 

# retrieved_group_date = get_group_date(group_date_id)
# if retrieved_group_date:
#     print("Retrieved Group Date:")
#     print(retrieved_group_date)
######################################################################################################################
