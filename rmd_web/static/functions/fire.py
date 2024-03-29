import firebase_admin
from firebase_admin import credentials, firestore, storage
from google.cloud.firestore_v1.base_query import FieldFilter
import datetime
from google.cloud.firestore_v1 import ArrayUnion
# Initialize Firebase Admin SDK
db = firestore.client()

######################################################################################################################
# PROFILE

def get_user_profile(user_id):
    doc_ref = db.collection('profiles').document(user_id)
    doc = doc_ref.get()
    if doc.exists:
        # print(doc.to_dict())
        return doc.to_dict()
    else:
        print(f"No user profile found for email: {user_id}")
        return None

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

def fetch_profile(profile_id):
    profile_ref = db.collection('profiles').document(profile_id)
    profile_data = profile_ref.get().to_dict()
    # print(profile_data)
    return profile_data
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

######################################################################################################################

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
    
    # print("term:", term)
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

######################################################################################################################
# UPLOAD_IMAGE

def image_upload(uploaded_image,folder):
    # print('upload_image',uploaded_image)
    # print('upload_image.name',uploaded_image.name)
    
    bucket = storage.bucket()
    blob = bucket.blob(folder+ '/' + uploaded_image.name)  # Replace with the desired path and name for the uploaded image in Firebase Storage
    blob.upload_from_file(uploaded_image)
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
    profiles_ref = db.collection("profiles")
    id_ref = profiles_ref.where(filter=FieldFilter("id", "==", term))
    first_name_ref = profiles_ref.where(filter=FieldFilter("first_name", "==", term))
    last_name_ref = profiles_ref.where(filter=FieldFilter("last_name", "==", term))
    email_ref = profiles_ref.where(filter=FieldFilter("email", "==", term))
    
    id_results = id_ref.stream()
    first_name_results = first_name_ref.stream()
    last_name_results = last_name_ref.stream()
    email_results = email_ref.stream()

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

######################################################################################################################
# 

######################################################################################################################

######################################################################################################################
# 


######################################################################################################################
