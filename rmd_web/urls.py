from django.urls import path
from . import views
from .views import home, event_or_date, messages,profiles, search_results



urlpatterns = [
######################################################################################################################
    # path('', views.home, name="home"),
    path('', home, name="home"),
    path('get_group_date', event_or_date.get_group_date, name="get_group_date"),
######################################################################################################################
# PROFILE
    # path('profile/', views.profile, name="profile"),
    path('profile/', profiles.user_profile, name="user_profile"),
    path('create_profile/', profiles.create_user, name="create_profile"),
    path('edit_profile/', profiles.edit_user, name="edit_profile"),
    # path('view_profile/', views.get_individuals_profile, name="view_profile"),
    # path('view_profile/<int:profile_id>/', views.view_profile, name='view_profile'),
    # path('profile/<str:profile_id>/', views.profile_view, name='profile_view'),
    path('profile/<str:email>/', profiles.profile_view, name='profile_view'),
######################################################################################################################

######################################################################################################################
# MESSAGES
    path('message/', messages.conversations, name='messages'),
    path('send_message/', messages.send_message, name='send_message'),
######################################################################################################################

######################################################################################################################
# SEARCH
    path('search/', search_results.get_search_results, name='search_results'),
######################################################################################################################

######################################################################################################################
# IMAGE UPLOAD
    # path('upload/', views.upload_image, name='upload_image'),
######################################################################################################################

######################################################################################################################
# POSTS
    path('add_comment/<post_id>/', views.add_comment, name='add_comment'),
    path('like_post/<post_id>/', views.like_post, name='like_post'),
    path('dislike_post/<post_id>/', views.dislike_post, name='dislike_post'),
######################################################################################################################

######################################################################################################################
# AUTH
    # path('signup/', views.signup, name='signup'),
######################################################################################################################

######################################################################################################################
# GROUP EVENTS
    path('create_event/', event_or_date.create_event, name='create_event'),
######################################################################################################################

]
