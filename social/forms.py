from django import forms
from django.core.exceptions import ValidationError
from django.forms import Textarea, FileInput
from .models import Image, Comment
from urllib import request
from django.core.files.base import ContentFile
from django.utils.text import slugify


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

    def __init__(self, *args, **kwargs):
        """Save the request with the form so it can be accessed in clean_*()"""
        self.request = kwargs.pop('request', None)
        super(CommentForm, self).__init__(*args, **kwargs)

    def clean_name(self):
        """Make sure people don't use my name"""
        data = self.cleaned_data['name']
        if not self.request.user.is_authenticated and data.lower().strip() == 'samuel':
            raise ValidationError("Sorry, you cannot use this name.")
        return data


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image', 'description']

    def __init__(self, *args, **kwargs):
        super(CreatePostForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget = Textarea(attrs={
            'class': 'field'})
        self.fields['image'].widget = FileInput(attrs={
            'id': 'file'
        })