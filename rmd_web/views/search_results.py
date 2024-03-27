from django.shortcuts import render,get_object_or_404
from django.core.exceptions import MultipleObjectsReturned
from django.http import JsonResponse, HttpResponse, HttpResponseServerError
from django.shortcuts import render, redirect
from django.contrib import messages

######################################################################################################################
# STATIC.FUNCTIONS
from ..static.functions.search import search_profiles_single_term,search_profiles
from ..static.functions.friend_request import send_friend_request, accept_friend_request, decline_friend_request, get_user_friend_request
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


def get_search_results(request):
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
  