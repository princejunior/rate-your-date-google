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
