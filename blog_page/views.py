from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic.edit import FormView
from django.views.generic import ListView, DetailView
from django.views import View
from django.utils.decorators import method_decorator

from .forms import BlogForm
from .models import Blog
from user.models import User
from tag.models import Tag
from followers.models import Followers
from user.decorators import login_required
# Create your views here.



class HomePage(View):
    def get(self, request):

        return render(request,'homepage.html', {'username': request.session.get('user')})

class IndexView(View):
    def get(self, request):
        blogs = Blog.objects.all().order_by('-id')[:5]
        return render(request, 'index.html', {'username': request.session.get('user'), 'blogs':blogs})

class FollowerBlogView(View):
    def get(self, request):
        username = request.session.get('user')
        if username == None:
            blogs = []
        else:
            user = User.objects.get(username=username)
            followee, _ = Followers.objects.get_or_create(follower=user)
            followee = followee.followee.all()
            blogs = Blog.objects.filter(writer__in=followee).all().order_by('-id')
            print(blogs)
        return render(request, 'follower_blogs.html',{'username': request.session.get('user'), 'blogs':blogs})

@method_decorator(login_required, name='dispatch')
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
        else:
            follow_bool = False
        return render(request, 'other_blog.html',  {'username': username,'blogs':blogs,'writer':writer,'follow_bool':follow_bool})



class RelationCreateView(View):
    def post(self, request):
        username = request.session.get('user')

        if username == None:
            return JsonResponse({'result': 'fail'})
        writer = request.POST.get('followee',None)

        if writer == None:

            return JsonResponse({'result': 'fail'})
        writer = User.objects.get(username=writer)
        tt = request.POST.get('tt',None)
        if tt == '0':
            user = User.objects.get(username=username)
            followee, _ = Followers.objects.get_or_create(follower=user)
            followee.followee.add(writer)
            followee.save()
        elif tt == '1':
            user = User.objects.get(username=username)
            followee, _ = Followers.objects.get_or_create(follower=user)
            followee.followee.remove(writer)
            followee.save()
        return JsonResponse({'result':"success"})

class BlogDetail(DetailView):
    template_name = "blog_detail.html"
    queryset = Blog.objects.all()
    context_object_name = "blog"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.request.session.get('user')
        return context


@method_decorator(login_required, name='dispatch')
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