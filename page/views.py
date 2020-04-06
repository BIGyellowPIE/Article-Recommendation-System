from django.shortcuts import render
from django.shortcuts import redirect
from . import models

def index(request):
    user_list = models.User.objects.all()
    return render(request, 'page/index.html',{"user_list":user_list})