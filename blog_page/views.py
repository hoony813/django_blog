from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.views.generic import ListView, DetailView
from django.views import View

from .forms import BlogForm
from .models import Blog
from user.models import User
from tag.models import Tag
from followers.models import Followers
# Create your views here.


class IndexView(View):
    def get(self, request):
        blogs = Blog.objects.all().order_by('-id')[:5]
        return render(request, 'index.html', {'username': request.session.get('user'), 'blogs':blogs})

class MyBlogList(ListView):
    template_name = 'my_blog.html'
    context_object_name = 'blogs'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.request.session.get('user')
        return context

    def get_queryset(self, **kwargs):
        queryset = Blog.objects.filter(writer__username=self.request.session.get('user'))
        return queryset

class BlogList(View):
    def get(self, request, writer=None):
        username = request.session.get('user')
        if writer == username:
            return redirect('/myblog/')
        blogs = Blog.objects.filter(writer__username=writer)
        followee = []
        if username != None:
            user = User.objects.get(username=username)

            followee, _ = Followers.objects.get_or_create(follower=user)

            followee = list(followee.followee.values('username'))

            follow_bool = {'username':writer} in followee



        return render(request, 'other_blog.html',  {'username': username,'blogs':blogs,'writer':writer,'follow_bool':follow_bool})


class BlogDetail(DetailView):
    template_name = "blog_detail.html"
    queryset = Blog.objects.all()
    context_object_name = "blog"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.request.session.get('user')
        return context


class BlogWrite(FormView):
    template_name = 'blog_write.html'
    form_class = BlogForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.request.session.get('user')
        return context

    def form_valid(self, form):

        print(self.request.FILES.get('image','blank.png'))
        user = User.objects.get(username=self.request.session.get('user'))
        blog = Blog(
            title=form.data.get('title'),
            contents=form.data.get('contents'),
            thumbnails=self.request.FILES.get('image','blank.png'),
            writer=user,
        )
        blog.save()
        tags = form.data.get('tags').split(',')
        for tag in tags:
            if not tag:
                continue
            _tag, _ = Tag.objects.get_or_create(name=tag)
            blog.tags.add(_tag)

        return super().form_valid(form)