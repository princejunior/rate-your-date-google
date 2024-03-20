from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    
######################################################################################################################
# PROFILE
    path('profile/', views.profile, name="profile"),
    path('create_profile/', views.create_user, name="create_profile"),
    path('edit_profile/', views.edit_user, name="edit_profile"),
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
# POSTS
path('add_comment/<post_id>/', views.add_comment, name='add_comment'),
path('like_post/<post_id>/', views.like_post, name='like_post'),
path('dislike_post/<post_id>/', views.dislike_post, name='dislike_post'),
######################################################################################################################

######################################################################################################################
# MESSAGES
path('message/', views.messages, name='messages'),

path('send_message/', views.send_message, name='send_message'),
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

]