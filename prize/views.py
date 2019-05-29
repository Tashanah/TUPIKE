from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404
from django.contrib.auth.decorators import login_required
import datetime as dt 
from .models import *
from django.contrib.auth.models import User
from . forms import UserUploadProjects,RatingsForms
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



def projects(request,project_id):
    try:
         projects=Projects.objects.get(id=project_id)
         all=Ratings.objects.filter(project=project_id)
    except Exception as e:
        raise Http404()


    count=0
    for i in all:
        count+=i.usability
        count+=i.design
        count+=i.content

    if count>0:
        average=round(count/3,1)
    else:
        average=0

    if request.method=='POST':
        form=RatingsForms(request.POST)
        if form.is_valid():
            rate=form.save(commit=False)
            rate.user=request.user
            rate.project=project_id
            rate.save()
        return redirect('projects',project_id)
    else:
        form=RatingsForms()


    votes=Ratings.objects.filter(project=project_id)
    usability=[]
    design=[]
    content=[]

    for i in votes:
        usability.append(i.usability)
        design.append(i.design)
        content.append(i.content)

    if len(usability)>0 or len(design)>0 or len(content)>0:
        average_usability=round(sum(usability)/len(usability),1)     
        average_design=round(sum(design)/len(design),1)     
        average_content=round(sum(content)/len(content),1)     

        average_rating=round((average_content+average_design+average_usability)/3,1)

    else:
        average_content=0.0
        average_design=0.0
        average_rating=0.0
        average_usability=0.0

    arr1=[]
    for use in votes:
        arr1.append(use.user_id)

    auth=arr1

        
    return render(request,'singlepost.html',{
        'projects':projects,
        'form':form,
        'usability':average_usability,
        'design':average_design,
        'content':average_content,
        'average_rating':average_rating,
        'auth':auth,
        'all':all,
        'average':average,
      
        }
)



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

        permission_classes = (IsAdminOrReadOnly,)

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

        permission_classes = (IsAdminOrReadOnly,)
