from django.shortcuts import render,get_object_or_404
from django.core.exceptions import MultipleObjectsReturned
from django.http import JsonResponse, HttpResponse, HttpResponseServerError
from django.shortcuts import render, redirect
from django.contrib import messages
import json
######################################################################################################################
# STATIC.FUNCTIONS
from ..static.functions.messages import get_messages, send_messages
from ..static.functions.check_sessions import check_user_data_session,check_user_messages_data_session

######################################################################################################################
# MESSAGES

def conversations(request):
    user_id = request.user.email
    user_data = check_user_data_session(request, user_id)
    # Deserialize user_data string into a dictionary
    user_data_dict = json.loads(user_data)

    # Now you can access the conversations
    conversations = user_data_dict.get('conversations', {})
    conversations_ids = conversations.get('messages_ids', [])
    # print(conversations_ids)
    
    messages, chat_with_other_user_id = get_messages(conversations_ids, user_id)
    print('messages', messages)
    context = {
        # 'user_conversations': user_conversations
        'user_conversations': messages,
        'current_user_id': user_id,
        'chat_with_other_user_id': chat_with_other_user_id
    }
    
    return render(request, 'pages/messages.html', context)

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
