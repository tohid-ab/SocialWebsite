from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.conf import settings
from django.views.generic import TemplateView, DetailView, CreateView, ListView
from .mixins import FormValidMixin
from django.contrib.auth.decorators import login_required
from .models import Image, Like, Comment
from .forms import CommentForm, CreatePostForm
from django.http import JsonResponse
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import FormView

# Create your views here.


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
    if request.user.is_authenticated:
        posts = Image.objects.all()
        liked_posts = []
        comments = CommentForm()

        for liked_post in request.user.likes.all():
            liked_posts.append(liked_post.post_id)

        return render(request, 'main/index.html', {'posts': posts, 'liked_posts': liked_posts, 'comments': comments})
    else:
        return redirect('login')


class ImageCreateView(FormValidMixin, CreateView):
    form_class = CreatePostForm
    template_name = 'post/creat_post.html'


class PostDetailView(DetailView):
    model = Image
    template_name = 'main/post_detail.html'
    context_object_name = 'post'

    def get_absolute_url(self):
        return reverse('post-detail', args=[str(self.pk)])

    def get(self, request, *args, **kwargs):
        view = PostDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PostComment.as_view()
        return view(request, *args, **kwargs)


class PostDisplay(DetailView):
    model = Image
    template_name = 'main/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context


class PostComment(SingleObjectMixin, FormView):
    model = Image
    form_class = CommentForm
    template_name = 'main/post_detail.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(PostComment, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.post = self.object
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        post = self.get_object()
        return reverse('post-detail', kwargs={'pk': post.pk}) + '#comments'