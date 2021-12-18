from django.urls import path
from .views import *

urlpatterns = [
    path('', posts, name='Home'),
    path('post/like/', like, name='like-post'),
    path('users/<str:username>/', UserDetailView.as_view(), name='user_detail'),
    path('create/', ImageCreateView.as_view(), name='create'),
]