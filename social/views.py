from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, DetailView, CreateView, ListView
from .mixins import FormValidMixin
from django.contrib.auth.decorators import login_required
from .models import Image, Like
from django.http import JsonResponse
# Create your views here.


# class Home(TemplateView):
#     template_name = 'main/index.html'
#     success_url = reverse_lazy('Home')
#
#     def get_context_data(self, *args, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['posts'] = Image.objects.all().order_by('-created')
#         context['liked_posts'] = Like.objects.all()
#         context['image_profile'] = Profile.objects.all()
#         return context


@login_required
def like(request):
    post_id = request.POST['post_id']
    post = Image.objects.get(pk=post_id)
    liked = True

    like_object, created = Like.objects.get_or_create(user_id=request.user, post_id=post)
    if not created:
        like_object.delete()  # the user already liked this picture before
        liked = False

    return JsonResponse({'liked': liked})


def posts(request):
    posts = Image.objects.all()
    liked_posts = []

    for liked_post in request.user.likes.all():
        liked_posts.append(liked_post.post_id)

    return render(request, 'main/index.html', {'posts': posts, 'liked_posts': liked_posts})


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