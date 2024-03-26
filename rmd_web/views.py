from django.shortcuts import render,get_object_or_404
from django.core.exceptions import MultipleObjectsReturned
from django.http import JsonResponse, HttpResponse, HttpResponseServerError
from django.shortcuts import render, redirect
from django.contrib import messages

######################################################################################################################
# STATIC.FUNCTIONS
from .static.functions.fire import get_user_profile, create_user_profile, edit_user_profile
from .static.functions.fire import get_user_post, get_friends_posts, fetch_profile, get_user_events, add_post, add_comment, like_post,dislike_post 
from .static.functions.fire import image_upload, get_messages, send_messages, search_profiles, search_profiles_single_term
from .static.functions.fire import get_user_friend_request, send_friend_request, accept_friend_request, decline_friend_request
from .static.functions.fire import create_group_date

from .static.functions.search import search_users
# from .static.functions.ads import
# from .static.functions.friend_request import
# from .static.functions.group_events import
# from .static.functions.messages import
# from .static.functions.friend_request import
# from .static.functions.post import


######################################################################################################################
# HOME
def home(request):
    # print(request.user.uid)
    if request.user.is_authenticated:
        print(request.user.is_authenticated)
        user_id = request.user.email
        user_information = get_user_profile(user_id)
        friend_requests = user_information.get('friend_requests', [])
        # print(friend_requests)
        friends = user_information.get('friends', [])  # Retrieve the 'friends' list or an empty list if not present
        # print(friends)
        # friend_requests = get_user_friend_request(user_information)
        # all_friends_posts = get_friends_posts(friends)
        all_friends_posts = get_friends_posts('elliott.t.elijah@gmail.com')
    
        if request.method == 'POST':
            print("Post button was clicked")
        
            action = request.POST.get('action')
            print('action', action)
            if action == 'add_post':
                print("add_post button was clicked")
                target_user_id = user_id
                post_content = request.POST.get('comment')
                post_image_url = request.FILES.get('picture')
                add_post(user_id, target_user_id, post_content,post_image_url)
                return redirect('profile')
        
            if action == 'like':
                print("like_post button was clicked")
                post_id = request.POST.get('post_id')
            
                like_post(post_id, user_id) 
                print("post ID", post_id)
                # pass
                return redirect('profile')

            if action == 'dislike':
                print("dislike_post button was clicked")
                post_id = request.POST.get('post_id')
                dislike_post(post_id,user_id)
                return redirect('profile')
        
            if action == 'comment':
                print("comment button was clicked")
            
                # add_comment()
                return redirect('profile')
            
            if action == 'search':
                print("search button was clicked")
                search_value = request.POST.get('search')
                print("search value", search_value)
                search_profiles_single_term(search_value)
                # search_profiles(search_value)
                return redirect('search_results')
            
            if action == "accept_friend_request":
                # Example of handling friend request decline
                array_placement_id = request.POST.get('array_id')
                print('array_placement_id', array_placement_id)
                sender_email = request.POST.get('sender_id')
                recipient_email = request.user.email  # Assuming recipient is the current user

                # Call the decline_friend_request function
                result = accept_friend_request(sender_email, recipient_email)
                
            if action == "decline_friend_request":
                # Example of handling friend request decline
                sender_email = request.POST.get('sender_id')
                recipient_email = request.user.email  # Assuming recipient is the current user

                # Call the decline_friend_request function
                result = decline_friend_request(sender_email, recipient_email)
    
        context = {
            'user_information': user_information,
            'friends':friends,
            'friend_posts': all_friends_posts, 
            'friend_requests': friend_requests
        }

        return render(request, 'home.html', context)
    else:
        user_id = None
        context = {
            'user_information': user_id,
            'friend_posts': None,
            'friend_requests': None
        }
        return render(request, 'home.html', context)

######################################################################################################################

######################################################################################################################
# PROFILE_&_USER
def user_profile(request):
    user_id = request.user.email
    profile_posts = get_user_post(request.user.email)
 
    user_information = get_user_profile(user_id)
    # profile_events = get_user_events(user_information['events'])
    events, dates = get_user_events(user_information['events'])
    if request.method == 'POST':
        print("Post button was clicked")
        
        action = request.POST.get('action')
        print('action', action)
        if action == 'add_post':
            print("add_post button was clicked")
            target_user_id = user_id
            post_content = request.POST.get('comment')
            post_image_url = request.FILES.get('picture')
            add_post(user_id, target_user_id, post_content,post_image_url)
            return redirect('profile')
        
        if action == 'like':
            print("like_post button was clicked")
            post_id = request.POST.get('post_id')
            
            like_post(post_id, user_id) 
            print("post ID", post_id)
            # pass
            return redirect('profile')

        if action == 'dislike':
            print("dislike_post button was clicked")
            post_id = request.POST.get('post_id')
            dislike_post(post_id,user_id)
            return redirect('profile')
        
        if action == 'comment':
            print("comment button was clicked")
            
            # add_comment()
            return redirect('profile')

        if action == 'create_group_date':
            print("create_group_date button was clicked")
            creator_id = request.user.email
            group_date_information =  {
                'creator_id': creator_id,
                'title': request.POST.get('title'), 
                'image': request.POST.get('image'), 
                'type_date_event' : request.POST.get('type_date_event'),
                'about_date': request.POST.get('about_date'), 
                'type': request.POST.get('type'),
                'specifications': request.POST.get('specifications'), 
                'start_date': request.POST.get('start_date'),
                'start_time': request.POST.get('start_time'),
                'end_date': request.POST.get('end_date'),
                'end_time': request.POST.get('end_time'),
                'maxParticipants': request.POST.get('maxParticipants'),
                'participants': request.POST.get('participants'),
                #friends/connections or for the public
                'privacy': request.POST.get('privacy'),
                #expired or not expired
                'expired': False, 
            }   
            
            create_group_date(group_date_information)
            
            return redirect('profile')
    context = {
       'user_information': user_information,
       'profile_posts': profile_posts,
       'profile_events': events,
       'profile_dates': dates,
       
    }
    # print(context)
    return render(request, 'profile/user_profile.html', context)


def profile(request):
    user_id = request.user.email
    profile_posts = get_user_post(request.user.email)
    # print("User's profile",request.user)
    user_information = get_user_profile(user_id)
    if request.method == 'POST':
        print("Post button was clicked")
        
        action = request.POST.get('action')
        print('action', action)
        if action == 'add_post':
            print("add_post button was clicked")
            target_user_id = user_id
            post_content = request.POST.get('comment')
            post_image_url = request.FILES.get('picture')
            add_post(user_id, target_user_id, post_content,post_image_url)
            return redirect('profile')
        
        if action == 'like':
            print("like_post button was clicked")
            post_id = request.POST.get('post_id')
            
            like_post(post_id, user_id) 
            print("post ID", post_id)
            # pass
            return redirect('profile')

        if action == 'dislike':
            print("dislike_post button was clicked")
            post_id = request.POST.get('post_id')
            dislike_post(post_id,user_id)
            return redirect('profile')
        
        if action == 'comment':
            print("comment button was clicked")
            
            # add_comment()
            return redirect('profile')

        if action == 'create_group_date':
            print("create_group_date button was clicked")
            creator_id = request.user.email
            group_date_information =  {
                'creator_id': creator_id,
                'title': request.POST.get('title'), 
                'image': request.POST.get('image'), 
                'type_date_event' : request.POST.get('type_date_event'),
                'about_date': request.POST.get('about_date'), 
                'type': request.POST.get('type'),
                'specifications': request.POST.get('specifications'), 
                'start_date': request.POST.get('start_date'),
                'start_time': request.POST.get('start_time'),
                'end_date': request.POST.get('end_date'),
                'end_time': request.POST.get('end_time'),
                'maxParticipants': request.POST.get('maxParticipants'),
                'participants': request.POST.get('participants'),
                #friends/connections or for the public
                'privacy': request.POST.get('privacy'),
                #expired or not expired
                'expired': False, 
            }   
            
            create_group_date(group_date_information)
            
            return redirect('profile')
    context = {
       'user_information': user_information,
       'profile_posts': profile_posts,
    }
    # print(context)
    return render(request, 'profile/profile.html', context)

def get_individuals_profile(request):
    # print(request.user)
    return render(request, 'profile/profile.html')
    
def create_user(request):
    email = request.user.email
    
    
    if request.method == 'POST':
        social_media = [
            request.POST.get('instagram'),
            request.POST.get('facebook'),
            ]

        user_profile_data = {
            'email': email,
            'first_name': request.POST.get('first_name'),
            'last_name': request.POST.get('last_name'),
            'profile_picture': request.FILES.get('profile_picture'),
            # 'profile_picture': profile_image_url,
            
            'professional_background': request.POST.getlist('professional_background'),
            'social_media': social_media,
            'interests': request.POST.getlist('interests'),
            'privacy_settings': {'email_visibility': request.POST.get('email_visibility')},
            'connections': [],
            'conversations': {'message_ids': []}, 
            'friends': []
        }
        create_user_profile(user_profile_data)
        return redirect('profile')  # Redirect to a page indicating profile creation success
    return render(request, 'profile/create_user.html')

def edit_user(request):
    # print(request.user.id)
    # print(request.user.email)
    
    user_id = request.user.email
    # user_id = str(request.user.id)

    if request.method == 'POST':
        social_media = [
            request.POST.get('instagram'),
            request.POST.get('facebook'),
        ]
        # print('Social Media', social_media)
        # Retrieve the profile picture from request.FILES
        profile_image = request.FILES.get('profile_picture')
        # Check if a profile picture was uploaded
        # print("profile_image", profile_image)
        
        if profile_image:
            profile_image_url = image_upload(profile_image,'profile')            
        else:
            profile_image_url = None  # Or provide a default URL if needed

        updated_data = {
            'first_name': request.POST.get('first_name'),
            'last_name': request.POST.get('last_name'),
            # 'profile_picture': request.POST.get('profile_picture'),
            'profile_picture': profile_image_url,
            'professional_background': request.POST.getlist('professional_background'),
            'social_media': social_media,
            'interests': request.POST.getlist('interests'),
            'privacy_settings': {'email_visibility': request.POST.get('email_visibility')}
        }
        edit_user_profile(user_id, updated_data)
        return redirect('profile')  # Redirect to a page indicating profile edit success
    return render(request, 'profile/edit_user.html')

# def view_profile(request, profile_id):
#     # Fetch the UserProfile object based on the profile_id
#     profile = get_object_or_404(UserProfile, pk=profile_id)
#     # Pass the profile object to the template for rendering
#     return render(request, 'view_profile.html', {'profile': profile})

def profile_view(request, profile_id):
    # Fetch profile data from Firestore
    profile_data = fetch_profile(profile_id)

    if not profile_data:
        return HttpResponse("Profile not found", status=404)

    return render(request, 'profile.html', {'profile': profile_data})
######################################################################################################################

######################################################################################################################
# FUNCTIONALITY PAGES
# def send_friend_request(request):
#     if request.method == 'POST':
#         sender_id = request.user.email
#         recipient_id = request.POST.get('recipient_id')
#         # Assume you have a Firestore collection named 'friend_requests'
#         send_friend_request(sender_id,recipient_id)
#         messages.success(request, 'Friend request sent successfully.')
#         return redirect('profile')  # Redirect to profile page after sending request
#     else:
#         return redirect('home')  # Redirect to home page if request method is not POST

def send_friend_request_view(request):
    if request.method == 'POST':
        sender_id = request.user.id
        receiver_id = request.POST.get('receiver_id')  # Assuming receiver_id is sent via POST
        send_friend_request(sender_id, receiver_id)
        # Add appropriate response or redirect here


def search_results(request):
    # Get the query parameter 'query' from the URL
    query_param = request.GET.get('query', '')
    # Get the query parameter 'search' from the URL
    search_param = request.GET.get('search', '')
    # print("Search_results",query_param, search_param)
    # Now you can use the query_param and search_param to fetch information
    # You can process the query and search parameters as needed
    search_result = search_profiles_single_term(query_param)
    # print(search_result)
    # For example, you can render a template with the query and search parameters
    
    
    if request.method == 'POST':
        sender_id = request.user.email
        recipient_id = request.POST.get('recipient_id')
        # print('sender_id', sender_id)
        # print('recipient_id', recipient_id)
        # Assume you have a Firestore collection named 'friend_requests'
        send_friend_request(sender_id, recipient_id)
        # messages.success(request, 'Friend request sent successfully.')
        
    context = {
        'query': query_param, 
        'search': search_param,
        'search_results' :  search_result
    }
    return render(request, 'pages/search_results.html', context)
######################################################################################################################
   
######################################################################################################################
# MESSAGES

def messages(request):
    messages = get_messages()
    return render(request, 'pages/messages.html', {'messages': messages})

# def get_messages(request):
#     messages = get_messages()
#     return render(request, 'pages/messages.html', {'messages': messages})

def send_message(request):
    if request.method == 'POST':
        user_id = request.user.email  # You should handle user authentication and get the user ID here
        message = request.POST['message']
        send_messages(user_id,message)
        return redirect('messages')
    return HttpResponse("Method Not Allowed", status=405)

######################################################################################################################
# AUTH
def signup(request):
    return render(request, 'account/signup.html')

######################################################################################################################

######################################################################################################################
# GROUP EVENT

def create_event(request):
    if request.method == 'POST':
        print("create_group_date button was clicked")
        creator_id = request.user.email
        group_date_information =  {
            'creator_id': creator_id,
            'title': request.POST.get('title'), 
            'image': request.POST.get('image'), 
            'type_date_event' : request.POST.get('event_date'),
            'about_date': request.POST.get('about_date'), 
            'type': request.POST.get('type'),
            'specifications': request.POST.get('specifications'), 
            'start_date': request.POST.get('start_date'),
            'start_time': request.POST.get('start_time'),
            'end_date': request.POST.get('end_date'),
            'end_time': request.POST.get('end_time'),
            'maxParticipants': request.POST.get('maxParticipants'),
            'participants': request.POST.get('participants'),
            #friends/connections or for the public
            'privacy': request.POST.get('privacy'),
            #expired or not expired
            'expired': False, 
        }       
        create_group_date(group_date_information)
        return redirect('profile')
    return render(request, 'pages/create_event_post.html')
    

######################################################################################################################

######################################################################################################################
# 

######################################################################################################################

######################################################################################################################
# 

######################################################################################################################

######################################################################################################################
# 

######################################################################################################################

######################################################################################################################
# 

######################################################################################################################

######################################################################################################################
# 

######################################################################################################################

######################################################################################################################
# 

######################################################################################################################

######################################################################################################################
# 

######################################################################################################################

######################################################################################################################
# 

######################################################################################################################

######################################################################################################################
def upload_image(request):
       if request.method == 'POST':
           # Get the uploaded image from the request
            uploaded_image = request.FILES['image']
            image_upload(uploaded_image)
       return render(request, 'image_upload.html')
######################################################################################################################

######################################################################################################################
# POSTS

# def create_post(request, username):
#     if request.method == 'POST':
#         post_data = {
#             'email': email,
#             'first_name': request.POST.get('first_name'),
#             'last_name': request.POST.get('last_name'),
#             'profile_picture': request.POST.get('profile_picture'),
#             'professional_background': request.POST.getlist('professional_background'),
#             'social_media': social_media,
#             'interests': request.POST.getlist('interests'),
#             'privacy_settings': {'email_visibility': request.POST.get('email_visibility')}
#         }
#         create_post(post_data)
#         return redirect('profile_created')  # Redirect to a page indicating profile creation success
    
    
#     if request.method == 'POST':
#         form = PostForm(request.POST)
#         if form.is_valid():
#             content = form.cleaned_data['content']
#             user_id = request.user.id  # Assuming you have user authentication set up properly

#             # Store the post in Firestore
#             db = firestore.client()
#             doc_ref = db.collection('posts').document()
#             doc_ref.set({
#                 'user_id': user_id,
#                 'content': content
#             })

#             return redirect('profile', username=username)
#     else:
#         form = PostForm()
#     return render(request, 'create_post.html', {'form': form})

# def add_comment(request, post_id):
#     # Implement adding a comment
#     # Retrieve the post using post_id
#     # Add a comment to the post
#     user_id = request.user.email
#     add_comment()
#     return JsonResponse({"success": True})

# def like_post(request, post_id):
#     # Implement liking a post
#     # Retrieve the post using post_id
#     # Increment the likes count for the post
#     return JsonResponse({"success": True})

# def dislike_post(request, post_id):
#     # Implement disliking a post
#     # Retrieve the post using post_id
#     # Increment the dislikes count for the post
#     return JsonResponse({"success": True})

######################################################################################################################
