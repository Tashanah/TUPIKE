from django.contrib import admin
from .models import Profile,Recipe,Category

class ImageAdmin(admin.ModelAdmin):
    admin.site.register(Profile)
    admin.site.register(Recipe)
    admin.site.register(Category)

# Register your models here.
