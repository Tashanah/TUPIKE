from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404
from django.contrib.auth.decorators import login_required
import datetime as dt 
from .models import *
from django.contrib.auth.models import User
from . forms import UserUploadRecipes,RatingsForms
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import  *
from .serializer import RecipesSerializer,ProfileSerializer
from rest_framework import status


@login_required(login_url='/accounts/login/')
def home(request):

    recipes=Recipe.objects.all()
    context = {
        "recipes":recipes,
    }

    return render(request,'recipe.html',context)

@login_required(login_url='/accounts/login/')
def post_recipe(request):
    current_user = request.user
    if request.method == 'POST':
        upload_form = UserUploadRecipes(request.POST, request.FILES)
        if upload_form.is_valid():
            home = upload_form.save(commit=False)
            home.profile =current_user  
            home.save()
        return redirect('home')
    else:
        upload_form = UserUploadRecipes()
            
    return render(request,'uploads.html',{"upload_form":upload_form,})

def comment(request):
    recipe_id = request.POST.get("id")
    recipe = Recipe.objects.get(pk=recipe_id)
    Comments.objects.create(user=request.user, recipe=recipe,
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
    
    recipes = Recipe.get_profile_recipes(profile.id)

    return render(request, 'user/profile.html', {"profile":profile,"profile_details": profile_details,"recipes":recipes})


def search_results(request):
    if 'profile' in request.GET and request.GET["profile"]:
        search_term = request.GET.get("profile")
        searched_profile = Recipe.search_by_profile(search_term)
        message = f"{search_term}"
        return render(request,'search.html',{"message":message,"profile":searched_profile})

    else:
        message = "Invalid input"
        return render(request,'search.html',{"message":message})



def recipe(request,recipe_id):
    recipes=Recipe.objects.get(id=recipe_id)
    location = recipes.food_image.url
    all=Ratings.objects.filter(recipe=recipe_id)
  


    count=0
    for i in all:
        count+=i.creativity
        count+=i.simplicity
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
            rate.recipe=recipe_id
            rate.save()
        return redirect('recipes',recipe_id)
    else:
        form=RatingsForms()


    votes=Ratings.objects.filter(recipe=recipe_id)
    creativity=[]
    simplicity=[]
    content=[]

    for i in votes:
        creativity.append(i.creativity)
        simplicity.append(i.simplicity)
        content.append(i.content)

    if len(creativity)>0 or len(simplicity)>0 or len(content)>0:
        average_creativity=round(sum(creativity)/len(creativity),1)     
        average_simplicity=round(sum(simplicity)/len(simplicity),1)     
        average_content=round(sum(content)/len(content),1)     

        average_rating=round((average_content+average_simplicity+average_creativity)/3,1)

    else:
        average_content=0.0
        average_simplicity=0.0
        average_creativity=0.0
        average_rating=0.0

    arr1=[]
    for use in votes:
        arr1.append(use.user_id)

    auth=arr1

        
    return render(request,'singlerecipe.html',{
        'recipes':recipes,
        'form':form,
        'content':average_creativity,
        'design':average_simplicity,
        'usability':average_content,
        'average_rating':average_rating,
        'auth':auth,
        'all':all,
        'average':average,
      
        }
)



class RecipesList(APIView):
    def get(self, request, format=None):
        all_recipes = Recipes.objects.all()
        serializers = RecipesSerializer(all_recipes, many=True)
        return Response(serializers.data)

       

    def post(self, request, format=None):
        serializers =RecipesSerializer(data=request.data)
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
