from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404
from django.contrib.auth.decorators import login_required
import datetime as dt 
from .models import *
from django.contrib.auth.models import User
from . forms import UserUploadProjects
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import  Projects,Profile
from .serializer import ProjectsSerializer,ProfileSerializer
from rest_framework import status

@login_required(login_url='/accounts/login/')
def home(request):

    projects=Projects.objects.all()
    context = {
        "projects":projects,
    }

    return render(request,'project.html',context)

@login_required(login_url='/accounts/login/')
def post_project(request):
    current_user = request.user
    if request.method == 'POST':
        upload_form = UserUploadProjects(request.POST, request.FILES)
        if upload_form.is_valid():
            home = upload_form.save(commit=False)
            home.profile =current_user
            upload_form.save()
        return redirect('home')
    else:
        upload_form = UserUploadProjects()
            
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

def profile(request,username):
    profile=User.objects.get(username=username)

    try:
        profile_details = Profile.get_by_id(profile.id)
    except:
        profile_details = Profile.filter_by_id(profile.id)
    
    projects = Projects.get_profile_projects(profile.id)

    return render(request, 'user/profile.html', {"profile":profile,"profile_details": profile_details,"projects":projects})


def search_results(request):
    if 'profile' in request.GET and request.GET["profile"]:
        search_term = request.GET.get("profile")
        searched_profile = Projects.search_by_profile(search_term)
        message = f"{search_term}"
        return render(request,'search.html',{"message":message,"profile":searched_profile})

    else:
        message = "Invalid input"
        return render(request,'search.html',{"message":message})

class ProjectsList(APIView):
    def get(self, request, format=None):
        all_projects = Projects.objects.all()
        serializers = ProjectsSerializer(all_projects, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers =ProjectsSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileList(APIView):
    def get(self, request, format=None):
        all_profile = Profile.objects.all()
        serializers = ProfileSerializer(all_profile, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers =ProfileSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)    

