from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('message/', views.home, name="message"),
    path('profile/', views.profile, name="profile"),
]