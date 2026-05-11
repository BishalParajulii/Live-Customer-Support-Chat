from django.urls import path
from . import views

urlpatterns = [
    path('<int:session_id>/', views.agent_join, name='agent_join'),
]
