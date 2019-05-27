from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404
from django.contrib.auth.decorators import login_required
import datetime as dt 
from .models import *
from . forms import UserUploadImage

@login_required(login_url='/accounts/login/')
def home(request):

    projects=Project.objects.all()
    context = {
        "projects":projects,
    }

    return render(request,'project.html',context)