from django.shortcuts import render
from django.http import JsonResponse
from django.views import View

from .models import Follwers
from user.models import User
# Create your views here.

class RelationCreate(View):
    def post(self, request):
        username = request.session.get('user')
        user = User.objects.get(username=username)
        relation, _ = Follwers.objects.get_or_create(follwer=user)

        followee = request.POST.get('id',None)
        if followee != None:
            followee = User.objects.get(username=followee)
            relation.followee.add(followee)
            relation.save()

        return JsonResponse()
