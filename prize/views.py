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

@login_required(login_url='/accounts/login/')
def post_project(request):
    current_user = request.user
    if request.method == 'POST':
        upload_form = UserUploadProject(request.POST, request.FILES)
        if upload_form.is_valid():
            home = upload_form.save(commit=False)
            home.profile =current_user
            upload_form.save()
        return redirect('home')
    else:
        upload_form = UserUploadProject()
            
    return render(request,'uploads.html',{"upload_form":upload_form,})

def comment(request):
    project_id = request.POST.get("id")
    project = Project.objects.get(pk=project_id)
    Comments.objects.create(user=request.user, project=project,
                            comm=request.POST.get("comment"))

    user = request.user.username
    comment = request.POST.get("comment")

    data = {"user": user, "comment": comment}
    return JsonResponse(data)



