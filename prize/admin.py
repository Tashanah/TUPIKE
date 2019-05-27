from django.contrib import admin
from .models import Profile,Projects

class ImageAdmin(admin.ModelAdmin):
    admin.site.register(Profile)
    admin.site.register(Projects)

# Register your models here.
