from django import forms
from .models import Image
from urllib import request
from django.core.files.base import ContentFile
from django.utils.text import slugify

#
# class ImageCreateForm(forms.ModelForm):
#     class Meta:
#         model = Image
#         fields = ('title', 'image', 'description')