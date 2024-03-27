from django.shortcuts import render,get_object_or_404
from django.core.exceptions import MultipleObjectsReturned
from django.http import JsonResponse, HttpResponse, HttpResponseServerError
from django.shortcuts import render, redirect
from django.contrib import messages

######################################################################################################################
# STATIC.FUNCTIONS
from ..static.functions.user_data import UserData


from ..static.functions.profile import get_user_profile, create_user_profile, edit_user_profile, fetch_profile
from ..static.functions.events_dates import create_group_date, participated_group_date, get_group_date, update_group_date,delete_group_date
from ..static.functions.events_dates import get_user_events
from ..static.functions.friend_request import send_friend_request, accept_friend_request, decline_friend_request, get_user_friend_request
from ..static.functions.post import get_user_post, get_friends_posts, add_post,like_post,dislike_post, add_comment
from ..static.functions.image_upload import image_upload

######################################################################################################################
# PROFILE_&_USER
def user_profile(request):
    user_id = request.user.email
    profile_posts = get_user_post(request.user.email)
   
    if 'user_data' in request.session:
        # Session contains user data
        user_data = request.session['user_data']
        # Proceed with your logic
        user_data = UserData(**user_data)  # Reconstruct UserData from the dictionary
    else:
        # Session is empty or does not contain user data
        user_information = get_user_profile(user_id)
        current_user_data = UserData(**user_information)
        request.session['user_data'] = current_user_data.to_dict()  # Convert UserData to a dictionary
        
        
    
    # if current_user_data.is_empty():
    #     user_information = get_user_profile(user_id)
    #     current_user_data = UserData(**user_information)
    #     friend_requests = current_user_data.get_friend_requests()
    #     friends = current_user_data.get_friends()  # Retrieve the 'friends' list or an empty list if not present
    #     all_friends_posts = get_friends_posts(friends)
    # else:
    #     print(current_user_data)
    #     # Handle the case when current_user_data is not empty
    #     pass  # You can add your logic here  
        
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
    #    'user_information': user_information,
       'user_information': request.session['user_data'],
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

def profile_view(request, email):
    # Fetch profile data from Firestore
    profile_id = email
    profile_data = fetch_profile(profile_id)
    profile_posts = get_user_post(profile_id)
 
    user_information = get_user_profile(profile_id)
    # profile_events = get_user_events(user_information['events'])
    events, dates = get_user_events(user_information['events'])
    if not profile_data:
        return HttpResponse("Profile not found", status=404)
    
    if request.method == 'POST':
        print("Post button was clicked")
        action = request.POST.get('action')
        print('action', action)
        if action == 'friend_request':
            sender_id = request.user.email
            recipient_id = profile_id
            send_friend_request(sender_id, recipient_id)
            return redirect('profile')
    # print(profile_data)
    context = {
       'profile_data': profile_data, 
       'profile_posts': profile_posts,
       'profile_events': events,
       'profile_dates': dates, 
    }

    return render(request, 'profile/view_profile.html', context)
######################################################################################################################
