from django.urls import path
from .views import *

urlpatterns = [
    path('', Home.as_view(), name='Home'),
    path('users/<str:username>/', UserDetailView.as_view(), name='user_detail'),
    path('create/', ImageCreateView.as_view(), name='create'),
]