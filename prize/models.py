from django.db import models
from django.contrib.auth.models import User
import datetime as dt
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    profile_photo=models.ImageField(upload_to='profiles/',default='download.jpeg')
    bio=models.TextField(max_length=500) 
    profile_name=models.CharField(max_length =30,blank=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE)


class Projects(models.Model):
   profile = models.ForeignKey(User,null=True,on_delete=models.CASCADE)
   title = models.CharField(max_length=20,blank=True)
   image_landing = models.ImageField(upload_to='landing/')
   description = HTMLField(max_length=200,blank=True)
   link = URLOrRelativeURLField(max_length=200)
   pub_date = models.DateTimeField(auto_now_add=True)


    @classmethod
   def get_profile_projects(cls,profile):
       projects = Projects.objects.filter(profile__pk=profile)
       print(projects)
       return projects

   @classmethod
   def search_by_projects(cls,search_term):
       projects = cls.objects.filter(title__icontains=search_term)
       return projects


   def __str__(self):
       return self.title

class Comments(models.Model):
    comm = models.CharField(max_length = 100, blank = True)
    image = models.ForeignKey(Image, related_name = "comments")


    def save_comment(self):
        self.save()

    def delete_comment(self):
        Comments.objects.get(id = self.id).delete()
    
    def update_comment(self,new_comment):
        comm = Comments.objects.get(id = self.id)
        comm.comment = new_comment
        comm.save()


