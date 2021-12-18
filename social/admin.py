from django.contrib import admin
from .models import Image, Like
from django.template.defaultfilters import truncatechars
# Register your models here.


class ImageAdmin(admin.ModelAdmin):
    list_display = ('get_description', 'user', 'image_tag', 'created',)
    list_filter = ('created',)
    prepopulated_fields = {'slug': ('title',)}

    def get_description(self, obj):
        return obj.description[:55]

    get_description.short_description = "description"


admin.site.register(Image, ImageAdmin)
admin.site.register(Like)