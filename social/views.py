from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, DetailView, CreateView, ListView
from django.urls import reverse_lazy
from .mixins import FormValidMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Image
from accounts.models import Profile
# Create your views here.


class Home(TemplateView):
    template_name = 'main/index.html'
    success_url = reverse_lazy('Home')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = Image.objects.all().order_by('-created')
        context['image_profile'] = Profile.objects.all()
        return context


class ImageCreateView(FormValidMixin, CreateView):
    model = Image
    template_name = 'post/creat_post.html'
    fields = ['image', 'description']


class UserDetailView(DetailView):
    model = get_user_model()
    template_name = 'main/user_detail.html'

    def get_object(self):

        object = get_object_or_404(User, username=self.kwargs.get("username"))

        if self.request.user.username == object.username:
            return object
        return self.request.user