"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from baton.autodiscover import admin
from datetime import datetime, timedelta, date

from blog_page.models import Blog
from .settings import MEDIA_URL, MEDIA_ROOT
from user.views import RegisterView, LoginView, logout
from blog_page.views import (
    HomePage,
    BlogWrite, IndexView, MyBlogList, BlogDetail, BlogList, RelationCreateView, FollowerBlogView
)

orig_index = admin.site.index
def blog_index(request, extra_context=None):
    base_date = datetime.now() - timedelta(days=6)
    blog_data = {}
    for i in range(7):
        target_dttm = base_date + timedelta(days=i)
        date_key = target_dttm.strftime("%Y-%m-%d")
        target_date = date(target_dttm.year, target_dttm.month, target_dttm.day)
        blog_cnt = Blog.objects.filter(registered_date__date=target_date).count()
        blog_data[date_key] = blog_cnt
    print(blog_data)
    extra_context = {
        'blogs': blog_data
    }
    return orig_index(request, extra_context)

admin.site.index = blog_index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('baton/', include('baton.urls')),
    path('recent-blog/', IndexView.as_view()),
    path('', HomePage.as_view()),
    path('logout/', logout, name='logout'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('blog/write/', BlogWrite.as_view(), name='blog_write'),
    path('blog/detail/<int:pk>/', BlogDetail.as_view(), name='blog_detail'),
    path('myblog/<str:writer>/', BlogList.as_view(), name='blog_list'),
    path('myblog/', MyBlogList.as_view(), name='myblog'),
    path('follow/', RelationCreateView.as_view()),
    path('blog/follower/', FollowerBlogView.as_view()),
]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)