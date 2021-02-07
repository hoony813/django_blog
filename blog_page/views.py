from django.shortcuts import render
from django.views.generic.edit import FormView

from .forms import BlogForm
# Create your views here.

class BlogWrite(FormView):
    template_name = 'blog_write.html'
    form_class = BlogForm