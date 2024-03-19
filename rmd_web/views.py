from django.shortcuts import render
from django.core.exceptions import MultipleObjectsReturned
from django.http import HttpResponseServerError

from django.shortcuts import render, redirect

######################################################################################################################
# STATIC.FUNCTIONS
from .static.functions.fire import get_user_profile, create_user_profile, edit_user_profile, image_upload
from .static.functions.friend_request import send_friend_request
from .static.functions.search import search_users
# from .static.functions.ads import
# from .static.functions.friend_request import
# from .static.functions.group_events import
# from .static.functions.messages import
# from .static.functions.friend_request import
# from .static.functions.post import

######################################################################################################################
def upload_image(request):
       if request.method == 'POST':
           # Get the uploaded image from the request
            uploaded_image = request.FILES['image']
            image_upload(uploaded_image)
    
        #    # Initialize Firebase
        #    cred = credentials.Certificate('path/to/serviceAccountKey.json')  # Replace with the path to your service account key JSON file
        #    firebase_admin.initialize_app(cred, {
        #        'storageBucket': 'your-bucket-name.appspot.com' # Replace with your Firebase Storage bucket name
        #    })
           # Upload Image
        #    bucket = storage.bucket()
        #    blob = bucket.blob('path/to/' + uploaded_image.name)  # Replace with the desired path and name for the uploaded image in Firebase Storage
        #    blob.upload_from_file(uploaded_image)

        #    print('Image uploaded successfully')


       return render(request, 'image_upload.html')
######################################################################################################################
# HOME
def home(request):
    print(request.user)
    context = {
       'user_information': get_user_profile(request.user.email)
    }
    return render(request, 'home.html', {'context': context})
######################################################################################################################

######################################################################################################################
# PROFILE_&_USER

def profile(request):
    print("User's profile" ,request.user)
    context = {
       'user_information': get_user_profile(request.user.email)
    }
    print(context)
    return render(request, 'profile/profile.html', {'context': context})

def get_individuals_profile(request):
    print(request.user)
    return render(request, 'profile/profile.html')
    
def create_user(request):
    email = request.user.email
    social_media = [
       request.POST.get('instagram'),
       request.POST.get('facebook'),
    ]
    if request.method == 'POST':
        user_profile_data = {
            'email': email,
            'first_name': request.POST.get('first_name'),
            'last_name': request.POST.get('last_name'),
            'profile_picture': request.POST.get('profile_picture'),
            'professional_background': request.POST.getlist('professional_background'),
            'social_media': social_media,
            'interests': request.POST.getlist('interests'),
            'privacy_settings': {'email_visibility': request.POST.get('email_visibility')}
        }
        create_user_profile(user_profile_data)
        return redirect('profile_created')  # Redirect to a page indicating profile creation success
    return render(request, 'profile/create_user.html')

def edit_user(request):
    print(request.user.id)
    print(request.user.email)
    
    
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
            profile_image_url = image_upload(profile_image)
            
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

######################################################################################################################

######################################################################################################################
# FUNCTIONALITY PAGES

def send_friend_request_view(request):
    if request.method == 'POST':
        sender_id = request.user.id
        receiver_id = request.POST.get('receiver_id')  # Assuming receiver_id is sent via POST
        send_friend_request(sender_id, receiver_id)
        # Add appropriate response or redirect here

def search_results(request):
    query = request.GET.get('query')
    if query:
        results = search_users(query)
    else:
        results = []
    return render(request, 'pages/search.html', {'results': results, 'query': query})
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
