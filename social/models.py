from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.html import format_html
from accounts.models import Profile
from django.utils.text import slugify
# Create your models here.


class Image(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='images_created', on_delete=models.CASCADE)
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='images_liked', blank=True)
    title = models.CharField(max_length=200, blank=True)
    slug = models.SlugField(max_length=200, blank=True)
    image = models.ImageField(upload_to='images/')
    description = models.TextField(blank=True)
    profile_image = models.ManyToManyField(Profile)
    created = models.DateField(auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return self.title

    def image_tag(self):
        return format_html("<img width=50 style='border-radius:5px;' src='{}'>".format(self.image.url))
    image_tag.short_description = 'عکس'

    def get_absolute_url(self):
        return reverse('profile')
