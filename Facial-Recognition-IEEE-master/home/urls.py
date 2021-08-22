from django.urls import path
from home.views import Index, webcam_feed
from . import views

urlpatterns = [
    path('', Index, name='index'),
    path('webcam_feed/', webcam_feed, name='webcam_feed'),
    path('signup/', views.register, name='register'),
    path('signup/2',views.register_face,name='register_face'),
    path('facecapture',views.signup_facecapture, name='signup_facecapture'),
]