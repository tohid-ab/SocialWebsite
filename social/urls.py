from django.urls import path
from .views import *


urlpatterns = [
    path('', posts, name='Home'),
    path('post/like/', like, name='like-post'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('create/', ImageCreateView.as_view(), name='create'),
]