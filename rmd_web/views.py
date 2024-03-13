from django.shortcuts import render
from django.core.exceptions import MultipleObjectsReturned
from django.http import HttpResponseServerError

# def my_view(request):
#     try:
#         # Code that may raise MultipleObjectsReturned exception
#         # ...
#     except MultipleObjectsReturned as e:
#         # Log the exception or handle it gracefully
#         # For example, you can return an error response to the user
#         return HttpResponseServerError("Multiple objects returned. Please contact the administrator.")

# Create your views here.
def profile(request):
    print(request.user)
    return render(request, 'profile/profile.html')
