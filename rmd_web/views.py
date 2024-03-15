from django.shortcuts import render
from django.core.exceptions import MultipleObjectsReturned
from django.http import HttpResponseServerError

from django.shortcuts import render, redirect

######################################################################################################################
# STATIC.FUNCTIONS
from .static.functions.fire import create_user_profile, edit_user_profile
from .static.functions.friend_request import send_friend_request

# from .static.functions.ads import
# from .static.functions.friend_request import
# from .static.functions.group_events import
# from .static.functions.messages import
# from .static.functions.friend_request import
# from .static.functions.post import

######################################################################################################################



######################################################################################################################
# HOME
def home(request):
    print(request.user)
    return render(request, 'home.html')
######################################################################################################################

######################################################################################################################
# PROFILE_&_USER

def profile(request):
    print(request.user)
    return render(request, 'profile/profile.html')

def get_user_profile(request):
    print(request.user)
    return render(request, 'profile/profile.html')
    
def create_user(request):
    if request.method == 'POST':
        user_profile_data = {
            'email': request.POST.get('email'),
            'fullName': request.POST.get('full_name'),
            'profilePicture': request.POST.get('profile_picture'),
            'professionalBackground': request.POST.getlist('professional_background'),
            'interests': request.POST.getlist('interests'),
            'privacySettings': {'email_visibility': request.POST.get('email_visibility')}
        }
        create_user_profile(user_profile_data)
        return redirect('profile_created')  # Redirect to a page indicating profile creation success
    return render(request, 'profile/create_user.html')

def edit_user(request, email):
    if request.method == 'POST':
        updated_data = {
            'fullName': request.POST.get('full_name'),
            'profilePicture': request.POST.get('profile_picture'),
            'professionalBackground': request.POST.getlist('professional_background'),
            'interests': request.POST.getlist('interests'),
            'privacySettings': {'email_visibility': request.POST.get('email_visibility')}
        }
        edit_user_profile(email, updated_data)
        return redirect('profile_edited')  # Redirect to a page indicating profile edit success
    return render(request, 'profile/edit_user.html')

######################################################################################################################

######################################################################################################################
# # views.py

def send_friend_request_view(request):
    if request.method == 'POST':
        sender_id = request.user.id
        receiver_id = request.POST.get('receiver_id')  # Assuming receiver_id is sent via POST
        send_friend_request(sender_id, receiver_id)
        # Add appropriate response or redirect here


######################################################################################################################
# 

######################################################################################################################

######################################################################################################################
# 

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
# 

######################################################################################################################

######################################################################################################################
# 

######################################################################################################################
