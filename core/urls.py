from django.contrib import admin
from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('send_message/', views.send_message),
    path("hook_receiver_view/", views.hook_receiver_view),
    
    path('whats/', views.webhook_verify, name="webhook_verify"),
    
    path('whats/post/', views.webhook, name="webhook"),
]
