from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    
######################################################################################################################
# PROFILE
    # path('profile/', views.profile, name="profile"),
    path('profile/', views.user_profile, name="user_profile"),
    # path('user_profile/', views.user_profile, name="user_profile"),
    
    path('create_profile/', views.create_user, name="create_profile"),
    path('edit_profile/', views.edit_user, name="edit_profile"),
    # path('view_profile/', views.get_individuals_profile, name="view_profile"),
    # path('view_profile/<int:profile_id>/', views.view_profile, name='view_profile'),
    path('profile/<str:profile_id>/', views.profile_view, name='profile_view'),
    # path('profile/<str:email>/', views.profile_view, name='profile_view'),
######################################################################################################################

######################################################################################################################
# 
    path('send_friend_request_view/', views.send_friend_request_view, name='send_friend_request_view'),
    path('send-friend-request/', views.send_friend_request, name='send_friend_request'),
    path('accept_friend_request/', views.send_friend_request, name='accept_friend_request'),
    path('accept_friend_request/', views.send_friend_request, name='accept_friend_request'),
    path('decline_friend_request/', views.send_friend_request, name='decline_friend_request'),

######################################################################################################################

######################################################################################################################
# SEARCH
    path('search/', views.search_results, name='search_results'),
######################################################################################################################

######################################################################################################################
# IMAGE UPLOAD
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
# AUTH
    path('signup/', views.signup, name='signup'),

######################################################################################################################

######################################################################################################################
# GROUP EVENTS

    path('create_event/', views.create_event, name='create_event'),


######################################################################################################################

######################################################################################################################
# 

######################################################################################################################

######################################################################################################################
# 

######################################################################################################################

]
