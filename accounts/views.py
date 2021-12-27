from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormView, UpdateView
from django.contrib.auth.forms import UserChangeForm
from .models import *
from social.models import Image
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .form import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm

# Create your views here.


def user_login(request):
    form = LoginForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated ', 'successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
        else:
            form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
            user_form.cleaned_data['password'])
            new_user.save()
        return render(request,'registration/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'user_form': user_form})


@login_required()
def profile_edit(request):
    Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        u_form = UserEditForm(request.POST, instance=request.user)
        p_form = ProfileEditForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Profile updated ', 'successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        u_form = UserEditForm(instance=request.user)
        p_form = ProfileEditForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'registration/edit_profile.html', context)


# class ProfileImageView(ListView):
#     model = Profile
#     template_name = 'main/index.html'
#     context_object_name = 'image'


class ProfileView(UpdateView):
    form_class = UserChangeForm
    success_url = reverse_lazy("Home")
    template_name = 'registration/profile.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = Image.objects.filter(user=self.object)
        # context['number'] = Post.objects.count() #نمایش تعداد پست ها
        return context

    def dispatch(self, request, *args, **kwargs):
        Profile.objects.get_or_create(user=request.user)
        if not request.user.is_authenticated:
            return redirect('login')
        return super(ProfileView, self).dispatch(request, *args, **kwargs)

    def get_object(self):
        return self.request.user
