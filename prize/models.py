from django.db import models
from django.contrib.auth.models import User
import datetime as dt
from django.db.models.signals import post_save
from django.dispatch import receiver
from tinymce.models import HTMLField
from url_or_relative_url_field.fields import URLOrRelativeURLField
from django.core.validators import MaxValueValidator


class Profile(models.Model):
    profile_photo=models.ImageField(upload_to='profiles/',default='download.jpeg')
    bio=models.TextField(max_length=500) 
    profile_name=models.CharField(max_length =30,blank=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE)

    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):
       if created:
           Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_profile(sender,instance,**kwargs):
       instance.profile.save()

    @classmethod
    def filter_by_id(cls,id):
        profile = Profile.objects.filter(user=id).first()
        return profile

    @classmethod
    def get_by_id(cls,id):
        profile=profile.objects.get(user=id)
        return profile



class Projects(models.Model):
   profile = models.ForeignKey(User,null=True,on_delete=models.CASCADE)
   title = models.CharField(max_length=20,blank=True)
   image_landing = models.ImageField(upload_to='landing/')
   description = HTMLField(max_length=200,blank=True)
   link = URLOrRelativeURLField(max_length=200)
   pub_date = models.DateTimeField(auto_now_add=True)
   design = models.IntegerField(default=0)
   usabilty = models.IntegerField(default=0)
   content = models.IntegerField(default=0)
    



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
    project = models.ForeignKey(Projects, related_name = "comments")


    def save_comment(self):
        self.save()

    def delete_comment(self):
        Comments.objects.get(id = self.id).delete()
    
    def update_comment(self,new_comment):
        comm = Comments.objects.get(id = self.id)
        comm.comment = new_comment
        comm.save()

class Ratings(models.Model):
    design = models.PositiveIntegerField(default=0,validators=[MaxValueValidator(10)])
    usability = models.PositiveIntegerField(default=0,validators=[MaxValueValidator(10)])
    content = models.PositiveIntegerField(default=0,validators=[MaxValueValidator(10)])
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    project = models.IntegerField(default=0)


