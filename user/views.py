from django.shortcuts import render
from django.views.generic.edit import FormView
from django.contrib.auth.hashers import make_password

from .forms import RegisterForm
from .models import User
# Create your views here.

class RegisterView(FormView):
    template_name = "register.html"
    form_class = RegisterForm
    success_url = '/'

    def form_valid(self, form):
        user = User(
            username = form.data.get('username'),
            email = form.data.get('email'),
            password = make_password(form.data.get('password')),
        )

        user.save()

        return super().form_valid(form)
