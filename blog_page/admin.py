from django.contrib import admin
from django.utils.html import format_html
from .models import Blog
# Register your models here.

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title','writer','registered_date')
    list_filter = ('writer',)
    ordering = ('-registered_date',)



admin.site.register(Blog, BlogAdmin)