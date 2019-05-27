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