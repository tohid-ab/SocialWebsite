from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .form import *
from .models import *
# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo']


admin.site.register(Profile, ProfileAdmin)