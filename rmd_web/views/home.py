from django.shortcuts import render,get_object_or_404
from django.core.exceptions import MultipleObjectsReturned
from django.http import JsonResponse, HttpResponse, HttpResponseServerError
from django.shortcuts import render, redirect
from django.contrib import messages

######################################################################################################################
# STATIC.FUNCTIONS
from ..static.functions.profile import get_user_profile, create_user_profile, edit_user_profile, fetch_profile
from ..static.functions.search import search_profiles_single_term,search_profiles
from ..static.functions.friend_request import send_friend_request, accept_friend_request, decline_friend_request, get_user_friend_request
from ..static.functions.post import get_user_post, get_friends_posts, add_post,like_post,dislike_post, add_comment
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
    # return render(request, 'home.html')

######################################################################################################################
