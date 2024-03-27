from django.shortcuts import render,get_object_or_404
from django.core.exceptions import MultipleObjectsReturned
from django.http import JsonResponse, HttpResponse, HttpResponseServerError
from django.shortcuts import render, redirect
from django.contrib import messages

######################################################################################################################
# STATIC.FUNCTIONS
from ..static.functions.events_dates import create_group_date, participated_group_date, get_group_date, update_group_date, delete_group_date

# from .static.functions.events_dates import create_group_date, participated_group_date, get_group_date, update_group_date,delete_group_date
# from .static.functions.events_dates import get_user_events
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
