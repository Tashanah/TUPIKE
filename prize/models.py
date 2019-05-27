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
