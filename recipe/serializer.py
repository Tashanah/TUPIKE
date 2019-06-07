from rest_framework import serializers
from .models import Profile, Recipe

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('profile_photo', 'bio', 'profile_name', 'user')

class RecipesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('profile', 'title', 'food_image', 'description', 'link')