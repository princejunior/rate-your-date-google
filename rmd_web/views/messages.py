from django.shortcuts import render,get_object_or_404
from django.core.exceptions import MultipleObjectsReturned
from django.http import JsonResponse, HttpResponse, HttpResponseServerError
from django.shortcuts import render, redirect
from django.contrib import messages

######################################################################################################################
# STATIC.FUNCTIONS
from ..static.functions.messages import get_messages, send_messages


######################################################################################################################
# MESSAGES

def conversations(request):
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
