from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from django.utils import timezone
from django.contrib import messages
from datetime import datetime
# GOOGLE
from google.cloud.firestore_v1 import SERVER_TIMESTAMP
from firebase_admin import firestore, storage
from allauth.account.signals import user_signed_up
from django.dispatch import receiver

# Import your models and forms
from .models import User, Person, Post, Comment
from .forms import SignUpForm, UserLoginForm, ReviewForm, PostForm, PersonForm, UserProfileForm

def google_signup(request):
    # Redirects the user to the Google login page provided by django-allauth
    return redirect('/accounts/google/login/')

@receiver(user_signed_up)
def after_user_signed_up(request, user, **kwargs):
    # Perform your custom actions here
    # For example, create a UserProfile instance for the new user
    pass

# AUTHENTICATION 
def signup(request):
    # Allow users to sign up and automatically log them in after signup.
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Save the user to Django database
            user = form.save()
            
            # Automatically log in the user after signup
            user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password1'])
            login(request, user)
            
            # Save the user's email to Firestore
            db = firestore.client()
            users_ref = db.collection(u'users')
            users_ref.document(str(user.id)).set({
                u'email': form.cleaned_data['email'],
                # Add other user information as needed
            })
            
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'auth/signup.html', {'form': form})

def user_login(request):
    # Authenticate and log in a user.
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                # Authentication failed, handle error
                # pass
                return render(request, 'auth/login.html', {'form': form})          
    else:
        form = UserLoginForm()
    return render(request, 'auth/login.html', {'form': form})

def user_logout(request):
    # Log out the current user.
    logout(request)
    return redirect('login')

# Profile and People Management
@login_required
def add_user_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            # Assuming you have initialized Firebase Admin SDK earlier in your project
            user_profile_data = form.cleaned_data

            # Handle the uploaded image file
            profile_picture = request.FILES.get('profile_picture')
            if profile_picture:
                # Construct a unique filename, could use the user's email or other unique identifier
                filename = f"profile_pictures/{user_profile_data['email']}_{profile_picture.name}"
                # Create a reference to the uploaded file in Firebase Storage
                blob = storage.bucket().blob(filename)
                blob.upload_from_string(
                    profile_picture.read(), 
                    content_type=profile_picture.content_type
                )
                blob.make_public()
                user_profile_data['profile_picture'] = blob.public_url

            # Extract interests and handle other form data for Firebase saving logic here
            print(user_profile_data)  # Placeholder for further Firebase logic

            return redirect('success_url')  # Redirect to a success page
    else:
        form = UserProfileForm()
    return render(request, 'profile/add_user_profile.html', {'form': form})

def user_profile(request, user_email):
    db = firestore.client()
    user_profile_doc = db.collection('user_profiles').document(user_email).get()
    if user_profile_doc.exists:
        user_profile_data = user_profile_doc.to_dict()
        return render(request, 'profile/user_profile.html', {'profile': user_profile_data})
    else:
        return render(request, 'profile/user_profile.html', {'error': 'User profile not found'})

@login_required
def edit_user_profile(request, user_email):
    db = firestore.client()
    document_reference = db.collection('user_profiles').document(user_email)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile_data = form.cleaned_data
            # Assume profile_picture handling and interests are included in form.cleaned_data
            document_reference.update(profile_data)
            return redirect('profile_view', user_email=user_email)  # Redirect to the profile view
    else:
        doc = document_reference.get()
        if doc.exists:
            form = UserProfileForm(initial=doc.to_dict())  # Pre-populate form with existing data
        else:
            form = UserProfileForm()  # Empty form if document does not exist

    return render(request, 'profiles/edit_profile.html', {'form': form, 'user_email': user_email})

# Create a new person profile. Only accessible to logged-in users.
@login_required
def create_person(request):
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            person = form.save(commit=False)
            person.user = request.user
            
            # Set joined_date to the current date
            current_date = timezone.now()
            person.joined_date = current_date
            
            # Save data to Firestore
            db = firestore.client()
            persons_ref = db.collection('people')
            doc_ref = persons_ref.add({
                'who_created_user_id': str(request.user.id),
                'first_name': person.first_name,
                'last_name': person.last_name,
                'joined_date': current_date,
                'instagram_id': person.instagram
            })
            
            # Retrieve the document ID (person ID)
            person_id = doc_ref.id

            # Redirect to the viewperson page with the person_id parameter
            return redirect('viewperson', person_id=person_id)

    else:
        form = PersonForm()
    
    return render(request, 'create/create_person.html', {'form': form, 'current_date': timezone.now().strftime('%Y-%m-%d')})

# def create_person(request):
#     if request.method == 'POST':
#         form = PersonForm(request.POST)
#         if form.is_valid():
#             person = form.save(commit=False)
#             person.user = request.user
            
#             # Set joined_date to the current date
#             current_date = timezone.now().strftime('%Y-%m-%d')
#             person.joined_date = current_date
            
#             person.save()
#             return redirect('viewperson', person_id=person.id)
#     else:
#         form = PersonForm()
    
#     return render(request, 'pages/create_person.html', {'form': form, 'current_date': timezone.now().strftime('%Y-%m-%d')})



# View a person's profile along with recent reviews. Requires login.
@login_required
def view_person(request, person_id):
    person_ref = firestore.client().collection('people').document(person_id)
    person_data = person_ref.get().to_dict()

    if not person_data:
        # If person with given ID doesn't exist in Firestore
        return redirect('explore')  # Or you can show an error page

    # Include the Firestore document ID inside person_data
    person_data['id'] = person_id

    # Retrieve recent posts for this person from Firestore
    recent_posts = firestore.client().collection('reviews').where('person_id', '==', person_id).order_by('time_created').stream()
    # Retrieve recent posts for this person from Firestore
    recent_reviews_ref = firestore.client().collection('reviews').where('person_id', '==', person_id).stream()

    # Initialize an empty list to store the retrieved review data
    recent_reviews = []

    # Iterate over the recent reviews and extract review data
    for review in recent_reviews_ref:
        review_data = review.to_dict()
        recent_reviews.append({
            'user_id': review_data.get('user_id', ''),  # Get user_id field or empty string if not found
            'comment': review_data.get('comment', ''),  # Get comment field or empty string if not found
            'how_met': review_data.get('how_met', ''),  # Get how_met field or empty string if not found
            'time_created': review_data.get('time_created', ''),  # Get time_created field or empty string if not found
            # Add other fields as needed
        })

    # Sort the person data list by time_created field
    recent_reviews.sort(key=lambda x: x['time_created'])

    # Print or return the sorted person data
    print(recent_reviews)

    
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            # Process form data when submitted
            review = review_form.save(commit=False)
            review.person_id = person_id  # Assigning person_id
            # print('review', review)
            # Check if user is authenticated before accessing username
            if request.user.is_authenticated:
                review.user = request.user
                try:
                     # Convert UUID to string
                    user_id_str = str(request.user.id)
                    # Save review data to Firebase Firestore
                    review_data = review_form.cleaned_data
                    firestore.client().collection('reviews').add({
                        'person_id': person_id,
                        'user_id': user_id_str,
                        'comment': review_data['content'],
                        'how_met': review_data['how_met'],
                        'time_created': SERVER_TIMESTAMP,  # Use Firestore's server timestamp
                    })
                    # print('reviewed data:', review_data)

                    messages.success(request, 'Review submitted successfully.')
                    return redirect('view_person', person_id=person_id)
                except Exception as e:
                    messages.error(request, f'Error saving review: {e}')
                    print("Error saving review:", e)
            else:
                messages.error(request, 'You need to be logged in to submit a review.')
        else:
            # Debug statement to check form errors
            print("Form errors:", review_form.errors)
            messages.error(request, 'Failed to submit review. Please check the form.')
    else:
        review_form = ReviewForm()

    context = {
        'user': request.user,
        'person': person_data,
        'recent_reviews': recent_reviews,  # Pass the reviews_ref data to the template
        'review_form': review_form
    }
    return render(request, 'pages/view_person.html', context=context)

# Search for people based on names or Instagram IDs. Requires login.
@login_required
def search_person(request):
    query = request.GET.get('query')
    results = []

    if query:
        # Perform search operation
        persons_ref = firestore.client().collection('people')
        query_results = persons_ref.where('first_name', '>=', query).where('first_name', '<=', query + '\uf8ff').stream()
        results = [{'id': doc.id, **doc.to_dict()} for doc in query_results]
        
        query_results = persons_ref.where('last_name', '>=', query).where('last_name', '<=', query + '\uf8ff').stream()
        results += [{'id': doc.id, **doc.to_dict()} for doc in query_results]
        
        query_results = persons_ref.where('instagram', '>=', query).where('instagram', '<=', query + '\uf8ff').stream()
        results += [{'id': doc.id, **doc.to_dict()} for doc in query_results]

    context = {
        'user': request.user,
        'results': results,
        'query': query
    }
    # print(results)
    # print(query)
    return render(request, 'pages/search_results.html', context=context)

# Explore page showing all people. Requires login.
@login_required
def explore(request):
    # Retrieve all documents from the "people" collection
    persons_ref = firestore.client().collection('people')
    persons_with_ids = []
    
    for doc in persons_ref.stream():
        person_data = doc.to_dict()
        person_data['id'] = doc.id  # Use document ID as person ID
        persons_with_ids.append(person_data)

    context = {
        'user': request.user,
        'persons': persons_with_ids,
    }
    return render(request, 'pages/explore.html', context=context)

# Render the page for creating a new person profile.
def createNewPerson(request):
    context = {
        'user': request.user  # Pass the user object to the context
    }
    return render(request, 'create/create_person.html', context=context)

# Create a new post associated with a person profile. Requires login.
@login_required
def create_post(request, person_id):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            # Create a new post instance but don't save it yet
            post = form.save(commit=False)
            # Assign the user and person IDs to the post instance
            post.user_id = request.user.id
            post.person_id = person_id
            # Now save the post instance
            post.save()
            return redirect('view_person', person_id=person_id)
    else:
        form = PostForm()
    return render(request, 'create/create_post.html', {'form': form})

# Add a comment to a post. Requires login.
@login_required
def add_comment(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        comment_text = request.POST.get('comment')
        post = get_object_or_404(Post, pk=post_id)
        # Create the comment
        comment = Comment(post=post, user=request.user, text=comment_text)
        comment.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

# Increment the agree count for a specific comment.
def agree_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.agree += 1
    comment.save()
    return redirect('post_detail', post_id=comment.post_id)


# Home page view that shows user-specific data if logged in.
def home(request):
    
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Get the ID of the logged-in user
        user_id = request.user.id
        # Access Firestore database
        db = firestore.client()

        # Fetch data from Firestore
        users_ref = db.collection(u'users')
        users = users_ref.get()

        user_data = []
        for user in users:
            user_data.append(user.to_dict())

        context ={
            'user_id': user_id,
            'user_data': user_data
        }
        # You can now use user_id in your template or perform other actions
        return render(request, 'pages/home.html', context=context)
    else:
        # Handle the case where the user is not authenticated
        # Redirect the user to the login page or display a message
        # return redirect('login')  # Assuming 'login' is the name of your login URL
        context ={
            'user_id': None,
            'user_data': None
        }
        # You can now use user_id in your template or perform other actions
        return render(request, 'pages/home.html', context=context)


def group_events(request):
    return render(request, 'pages/group_events.html')
    