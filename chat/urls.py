from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_room, name='chat_room'),
    path('<int:session_id>/', views.chat_join, name='chat_join'),
    path('<int:session_id>/rate/', views.submit_rating, name='submit_rating'),
]