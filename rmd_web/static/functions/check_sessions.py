from .user_data import UserData
from . import get_user_profile 
from django.core.serializers.json import DjangoJSONEncoder
import json

def check_user_data_session(request, user_id):
    if 'user_data' in request.session:
        # Session contains user data
        user_data = request.session['user_data']
        # Proceed with your logic
        # user_data = UserData(**user_data)  # Reconstruct UserData from the dictionary
        return user_data
    else:
        # Session is empty or does not contain user data
        user_information = get_user_profile(user_id)
        current_user_data = UserData(**user_information)
        request.session['user_data'] = current_user_data.to_dict()  # Convert UserData to a dictionary
        user_data = request.session['user_data']
        return  user_data
    
# def check_user_messages_data_session(request):
#     if 'user_data' in request.session:
#         user_data_dict = request.session['user_data']

#         if isinstance(user_data_dict, dict):
#             user_data = UserData.from_dict(user_data_dict)

#             if not user_data.messages_data:
#                 user_data.fetch_messages()

#             request.session['user_data'] = json.dumps(user_data.to_dict(), cls=DjangoJSONEncoder)

#             return user_data

#     print("No user data found in session or invalid format")
#     return None
    
def check_user_messages_data_session(request):
        # Assuming request is the Django request object
    if 'user_data' in request.session:
        user_data = request.session['user_data']

        # Fetch messages if needed
        if not user_data.messages_data:
            user_data.fetch_messages()

        # Store the updated user_data back in the session
        request.session['user_data'] = user_data

    # Now user_data.messages_data contains all messages
    else:
    # Handle case where 'user_data' key is not present in session
        print("No user data found in session")
    
    return request.session['user_data']


def update_user_data_messages():
    pass