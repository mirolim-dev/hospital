from django.contrib import admin
from django.utils.html import format_html

from .models import AboutProject, Feature, SubFeature
# Register your models here.

def display_image(obj):
    if obj.image:
        return format_html('<img src="{}" width="50" height="50"/>', obj.image.url)
    return "Image not found"

display_image.short_description = "Image"


class AboutProjectAdmin(admin.ModelAdmin):
    list_display = ['id', display_image, 'get_title', 'is_active', 'created_at']

    def get_title(self, obj):
        if len(obj.title) < 16: 
            return obj.title
        return obj.title[:15]
    
    get_title.short_description = "title"
admin.site.register(AboutProject, AboutProjectAdmin)


class FeatureAdmin(admin.ModelAdmin):
    list_display = ['display_name', display_image, 'created_at']

    def display_name(self, obj):
        if len(obj.name) < 16:
            return obj.name
        return obj.name[:15]
    display_name.short_description = "name"

admin.site.register(Feature, FeatureAdmin)


class SubFeatureAdmin(admin.ModelAdmin):
    list_display = ['feature', 'display_name', display_image, 'created_at']
    list_filter = ['feature']

    def display_name(self, obj):
        if len(obj.name) < 16:
            return obj.name
        return obj.name[:15]
    display_name.short_description = "name"

admin.site.register(SubFeature, SubFeatureAdmin)