from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('message/', views.home, name="message"),
    
######################################################################################################################
# PROFILE
    path('profile/', views.profile, name="profile"),
    path('create_user/', views.create_user, name="create_user"),
    path('edit_user/', views.edit_user, name="edit_user"),
    path('view_profile/', views.get_individuals_profile, name="view_profile"),

    
######################################################################################################################

######################################################################################################################
# 
path('send_friend_request/', views.send_friend_request_view, name='send_friend_request'),
######################################################################################################################

######################################################################################################################
# 
path('search/', views.search_results, name='search_results'),
######################################################################################################################

######################################################################################################################
# 
path('upload/', views.upload_image, name='upload_image'),
######################################################################################################################

######################################################################################################################
# 

######################################################################################################################

]